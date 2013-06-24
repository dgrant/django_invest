from __future__ import division
import unittest, csv, string, datetime
from numpy import floor, reshape, size, array, arange
from dateutil.relativedelta import relativedelta
import sys

def readFromCSV(fileName):
    """Reads in transactions from a CSV file."""
    fp = open(fileName)
    text = fp.readlines()
    fp.close()

    csvReader = csv.reader(text)
    line = csvReader.next()
    header = line
    id = ''
    transactions = []

    for line in csvReader:
        if line[0] != '':
            transaction = {}
            for i in xrange(len(line)):
                transaction[header[i]] = line[i]
            #fix up date
            year, month, date = tuple([int(x) for x in transaction['date'].split('-')])
            transaction['date'] = datetime.date(year, month, date)
            #fix up amount
            transaction['amount'] = float(transaction['amount'].translate(string.maketrans('',''),'$ ,'))

            transactions.append(transaction)

    return transactions

def calculateXIRRFromTransactions(transactions, doPrint=False):
    """
    This function requires a weird input format.

    @param transactions List    of dictionaries. Each dictionary has 3 keys,
    date, amount, and accont
    """
    cfs = {}
    dfs = {}
    cfall = []
    dfall = []
    inflows = {}
    outflows = {}
    for transaction in transactions:
        date = transaction['date']
        amount = transaction['amount']
        account = transaction['account']
        try:
            cfs[account]
        except:
            cfs[account] = []
            dfs[account] = []
        cfs[account].append(amount)
        cfall.append(amount)
        dfs[account].append(date)                
        dfall.append(date)

        if amount > 0:
            inflows[account] = inflows.get(account, 0) + amount
        else:
            outflows[account] = outflows.get(account, 0) + amount

    if doPrint:
        print "Annualized returns"
        print "From:",min(dfall),"to",max(dfall)
        print "="*80    
        for key in sorted(cfs.keys()):
            print str(key)+":", xirrPct(cfs[key], dfs[key])
        print "="*80
        print "Overall:", xirrPct(cfall, dfall)
        print "Capital Gains:"
        for key in cfs.keys():
            print str(key)+":", -(inflows[key]+outflows[key])
    
    return xirr(cfall, dfall)

def xirrPct(cash_flows, dates , yld=0.1, maxiter=50, numDecimals=2):
    formatString = "%."+str(numDecimals)+"f"
    return formatString%(100*xirr(cash_flows,dates,yld,maxiter))+'%'

def xirr(cash_flows, dates, yld=0.1, maxiter=50):
    """
    @param cash_flows list of cashflows
    @param dates list of datetime.date objects
    @param yld guess for rate of return
    @param maxiter maximum iterations
    """
    assert len(dates) == len(cash_flows)
    for date in dates:
        assert type(date) == datetime.date

    date_ordinals = array([x.toordinal() for x in dates])
    cash_flows = array(cash_flows)
    
    #number of years in cash flow FIXME: use max and min date, not first and last in list
    func = int(floor(yearfrac(dates[0], dates[-1])))
    if func == 0:
        func = 1
    #matlab: tf = func*(dates(:,loop)-dates(1,loop))/(datemnth(dates(1,loop),12*func,0,0)-dates(1,loop));
    tf = func*(date_ordinals - date_ordinals[0]) / (dates[0] + relativedelta(months = +12*func) - dates[0]).days

    # Determine the best guess for yld
    min_result = sys.maxint
    best_yld = None
    for yld in arange(-0.9, 1, 0.1):
        if yld == 0:
            continue
        result_f = abs(sum(cash_flows / ((1 + yld)**tf)))
        if result_f < min_result:
            min_result = result_f
            best_yld = yld

    yld = best_yld
    print "Using guess yld=", yld

    func = 2
    k = 1
    #Newton's Method
    while abs(func) > 1.e-6:
        #cash flow polynomial
        func = sum(cash_flows / ((1 + yld)**tf))
        #%(CF poly)'
        f_prime = -sum((cash_flows/((1 + yld)**tf)) * (tf/(1 +yld)))
        if f_prime == 0:
            yld = None
            break
        
        delta = -func/f_prime
        yld = yld + delta
        k += 1
        if k == maxiter + 1:
            print 'Number of maximum iterations reached.'
            print 'Please increase MAXITER or use different GUESS.'
            yld = None
            break
    return yld
    

def yearfrac(date1, date2):
    wYears = int(floor(abs((date1 - date2).days) / 365.))
    date1W = datetime.date(date1.year + wYears, date1.month, date1.day)
    numerator = (date1W - date2).days
    try:
        denominator = (date1W - datetime.date(date1W.year + 1, date1W.month, date1W.day)).days
    #-----handle weird leap year case
    except ValueError:
        date1W = date1W + datetime.timedelta(1)
        denominator = (date1W - datetime.date(date1W.year + 1, date1W.month, date1W.day)).days
    yearFraction = numerator / float(denominator)
    return yearFraction + wYears

class TestFunctions(unittest.TestCase):
    def test(self):
        cf = [-10000,2500,2000,3000,4000]
        df = [datetime.date(1987,01,12),
                    datetime.date(1988,02,14),
                    datetime.date(1988,03,03),
                    datetime.date(1988,06,14),
                    datetime.date(1988,12,01)]
        expected = 0.1006
        result = xirr(cf, df, 0.3)
        self.assertAlmostEqual(expected, result, 4)
        
    def testYearFrac(self):
        date1 = datetime.date(1987,01,12)
        date2 = datetime.date(1988,12,01)
        result = yearfrac(date1, date2)
        expected = 1.885245
        self.assertAlmostEqual(expected, result, 5)
        
    def testYearFracZero(self):
        date1 = datetime.date(2000,01,01)
        date2 = datetime.date(2000,01,01)
        result = yearfrac(date1, date2)
        expected = 0
        self.assertEqual(expected, result)
    
    def testYearFrac1Year(self):
        """Test a bunch of cases where the two dates are separated by 1 year"""
        for year in range(2000, 2020, 1):
            date1 = datetime.date(year,1,1)
            date2 = datetime.date(year+1,1,1)
            result = yearfrac(date1, date2)
            self.assertEqual(1, result)
        
    def testYearFrac1000Years(self):
        date1 = datetime.date(2000,01,01)
        date2 = datetime.date(3000,01,01)
        result = yearfrac(date1, date2)
        expected = 1000
        self.assertEqual(expected, result)
    
    def testYearFracAlmostFullLeapYear(self):
        date1 = datetime.date(2000,01,01)
        date2 = datetime.date(2000,12,31)
        result = yearfrac(date1, date2)
        expected = 364/365.
        self.assertEqual(expected, result)
    
    def testYearFracAlmostFullYear(self):
        date1 = datetime.date(2001,01,01)
        date2 = datetime.date(2001,12,31)
        result = yearfrac(date1, date2)
        expected = 364/365.
        self.assertEqual(expected, result)
    
    def testYearFracFeb29_1(self):
        date1 = datetime.date(2000,02,28)
        date2 = datetime.date(2000,02,29)
        result = yearfrac(date1, date2)
        expected = 1/366.
        self.assertEqual(expected, result)        
    
    def testYearFracFeb29_2(self):
        date1 = datetime.date(2000,02,29)
        date2 = datetime.date(2000,03,01)
        result = yearfrac(date1, date2)
        expected = 1/365.
        self.assertEqual(expected, result)        
        
if __name__ == "__main__":
    unittest.main()
    #fileName = sys.argv[1]
    #calculateXIRRFromCSV(fileName)
    #fileName = '/home/david/MyDocuments/Office/financial/clearsight/xirr.csv'
    
#    fileName = '/home/david/xirr.csv'
#    transactions = readFromCSV(fileName)
#    calculateXIRRFromTransactions(transactions, True)

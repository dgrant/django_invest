import unittest, re
from datetime import date, timedelta
import urllib

class Quoter(object):
    def getPrice(self, dateToCheck):
        raise

class YahooQuoter(Quoter):
    def __init__(self, fullYahooSymbol, caching=True):
        self.symbol = fullYahooSymbol
        self.cache = {}
        self.caching = caching

    def getCurrentPrice(self):
        url = "http://quote.yahoo.com/d/quotes.csv"
        query = (
            ('s' , self.symbol),
            ('f' , "nl1d1t1"),
        )
        query = '&'.join(map(lambda (var, val): '%s=%s' % (var, str(val)), query))

        #***** Fetch from Yahoo
        full_url = url + '?' + query
        fp = urllib.urlopen(full_url)
        print "opening url:", full_url
        lines = fp.readlines()
        fp.close()

        if len(lines) >= 1:
            line_array = lines[0].split(',')
            theDate = line_array[2]
            pattern = re.compile(r"(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<year>\d{4,4})")
            match = pattern.search(theDate)
            if match:
                value = float(line_array[1])
            else:
                raise Exception("Failed to get current price of %s" % (self.symbol))
        else:
            raise Exception("Failed to get current price of %s" % (self.symbol))
        return value


    def getPrice(self, dateToCheck):
        #TODO: Determine symbol with country code

        if self.caching and self.cache.has_key(dateToCheck):
            value = self.cache[dateToCheck]
            return value

        offset = timedelta(1)
        maxTries = 7
        numTries = 0
        match = False
        while not match and numTries < maxTries:
            #print "Quering yahoo for", dateToCheck
            #** Construct query
            url = 'http://ichart.finance.yahoo.com/table.csv'
            query = (
                ('s' , self.symbol),
                ('d' , dateToCheck.month-1),
                ('e' , dateToCheck.day),
                ('f' , dateToCheck.year),
                ('a' , dateToCheck.month-1),
                ('b' , dateToCheck.day),
                ('c' , dateToCheck.year),
            )
            query = '&'.join(map(lambda (var, val): '%s=%s' % (var, str(val)), query))

            #** Fetch from Yahoo
            full_url = url + '?' + query
            fp = urllib.urlopen(full_url)
            print "opening url:", full_url
            lines = fp.readlines()
            fp.close()

            #** Parse and check if we got a valid quote or a 404
            if len(lines) > 1:
                line_array = lines[1].split(',')
                pattern = re.compile(r"(?P<year>\d{4,4})\-(?P<month>\d{2,2})\-(?P<day>\d{2,2})")
                match = pattern.match(line_array[0])
                if match:
                    value = float(line_array[4])

            #** Go backwards in time one more day
            dateToCheck -= offset

            numTries += 1

        if numTries == maxTries:        
            raise Exception('No quote found')
        else:
            #print "added", value, "on", dateToCheck, "to cache"
            if self.caching:
                self.cache[dateToCheck] = value
            return value

class TestQuotes(unittest.TestCase):
    def testExchangeRates(self):
        quoter = YahooQuoter('USDCAD=X')
        price = quoter.getCurrentPrice()
        assert 0.5 < price < 1.6

    def testGetTSXQuote(self):
        quoter = YahooQuoter('xic.TO', caching=True)
        self.assertEquals(81.30, quoter.getPrice(date(2006,12,29)))
        self.assertEquals(81.30, quoter.getPrice(date(2006,12,30)))
        self.assertEquals(81.30, quoter.getPrice(date(2006,12,31)))
        self.assertEquals(81.30, quoter.getPrice(date(2007, 1, 1)))
        self.assertEquals(81.51, quoter.getPrice(date(2007, 1, 2)))
        self.assertEquals(80.11, quoter.getPrice(date(2007, 1, 3)))
        self.assertEquals(78.98, quoter.getPrice(date(2007, 1, 4)))
        self.assertEquals(78.60, quoter.getPrice(date(2007, 1, 5)))
        self.assertEquals(79.05, quoter.getPrice(date(2007, 1, 8)))
        self.assertEquals(14.09, quoter.getPrice(date(2009, 1, 1)))

    def testCache(self):
        """
        Test caching feature. Make sure that it is working by measuring speed
        """
        import time
        quoter = YahooQuoter('xic.TO', caching=True)
        self.assertEquals(79.05, quoter.getPrice(date(2007,1,8)))
        startTime = time.time()
        for i in xrange(100):
            self.assertEquals(79.05, quoter.getPrice(date(2007,1,8)))
        endTime = time.time() - startTime
        self.assertTrue(endTime < 2)

if __name__ == "__main__":
    unittest.main()

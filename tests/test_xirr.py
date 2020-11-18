import datetime

from django.test import TestCase

from common.xirr import yearfrac, xirr


class TestFunctions(TestCase):
    def test(self):
        cf = [-10000, 2500, 2000, 3000, 4000]
        df = [
            datetime.date(1987, 0o1, 12),
            datetime.date(1988, 0o2, 14),
            datetime.date(1988, 0o3, 0o3),
            datetime.date(1988, 0o6, 14),
            datetime.date(1988, 12, 0o1),
        ]

        expected = 0.1006
        result = xirr(cf, df, 0.3)
        self.assertAlmostEqual(expected, result, 4)

    def testYearFrac(self):

        date1 = datetime.date(1987,0o1,12)
        date2 = datetime.date(1988,12,0o1)
        result = yearfrac(date1, date2)
        expected = 1.885245
        self.assertAlmostEqual(expected, result, 5)

    def testYearFracZero(self):

        date1 = datetime.date(2000,0o1,0o1)
        date2 = datetime.date(2000,0o1,0o1)
        result = yearfrac(date1, date2)
        expected = 0
        self.assertEqual(expected, result)

    def testYearFrac1Year(self):
        """Test a bunch of cases where the two dates are separated by 1 year"""
        for year in range(2000, 2020, 1):
            date1 = datetime.date(year, 1, 1)
            date2 = datetime.date(year + 1, 1, 1)
            result = yearfrac(date1, date2)
            self.assertEqual(1, result)

    def testYearFrac1000Years(self):
        date1 = datetime.date(2000, 0o1, 0o1)
        date2 = datetime.date(3000, 0o1, 0o1)

        result = yearfrac(date1, date2)
        expected = 1000
        self.assertEqual(expected, result)

    def testYearFracAlmostFullLeapYear(self):

        date1 = datetime.date(2000,0o1,0o1)
        date2 = datetime.date(2000,12,31)
        result = yearfrac(date1, date2)
        expected = 364 / 365.0
        self.assertEqual(expected, result)

    def testYearFracAlmostFullYear(self):

        date1 = datetime.date(2001,0o1,0o1)
        date2 = datetime.date(2001,12,31)
        result = yearfrac(date1, date2)
        expected = 364 / 365.0
        self.assertEqual(expected, result)

    def testYearFracFeb29_1(self):
        date1 = datetime.date(2000, 0o2, 28)
        date2 = datetime.date(2000, 0o2, 29)

        result = yearfrac(date1, date2)
        expected = 1 / 366.0
        self.assertEqual(expected, result)

    def testYearFracFeb29_2(self):
        date1 = datetime.date(2000, 0o2, 29)
        date2 = datetime.date(2000, 0o3, 0o1)

        result = yearfrac(date1, date2)
        expected = 1 / 365.0
        self.assertEqual(expected, result)

    def testFromFile(self):
        pass
        # fileName = sys.argv[1]
        # calculateXIRRFromCSV(fileName)
        # fileName = '/home/david/MyDocuments/Office/financial/clearsight/xirr.csv'
        # fileName = '/home/david/xirr.csv'
        # transactions = readFromCSV(fileName)
        # calculateXIRRFromTransactions(transactions, True)


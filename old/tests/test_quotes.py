import datetime

from django.test import TestCase

from common.Quotes import YahooQuoter


class TestQuotes(TestCase):
    def testExchangeRates(self):
        quoter = YahooQuoter("USDCAD=X")
        price = quoter.getCurrentPrice()
        assert 0.5 < price < 1.6

    def testGetTSXQuote(self):
        quoter = YahooQuoter("xic.TO", caching=True)
        self.assertEqual(81.30, quoter.getPrice(datetime.date(2006, 12, 29)))
        self.assertEqual(81.30, quoter.getPrice(datetime.date(2006, 12, 30)))
        self.assertEqual(81.30, quoter.getPrice(datetime.date(2006, 12, 31)))
        self.assertEqual(81.30, quoter.getPrice(datetime.date(2007, 1, 1)))
        self.assertEqual(81.51, quoter.getPrice(datetime.date(2007, 1, 2)))
        self.assertEqual(80.11, quoter.getPrice(datetime.date(2007, 1, 3)))
        self.assertEqual(78.98, quoter.getPrice(datetime.date(2007, 1, 4)))
        self.assertEqual(78.60, quoter.getPrice(datetime.date(2007, 1, 5)))
        self.assertEqual(79.05, quoter.getPrice(datetime.date(2007, 1, 8)))
        self.assertEqual(14.09, quoter.getPrice(datetime.date(2009, 1, 1)))

    def testCache(self):
        """
        Test caching feature. Make sure that it is working by measuring speed
        """
        import time

        quoter = YahooQuoter("xic.TO", caching=True)
        self.assertEqual(79.05, quoter.getPrice(datetime.date(2007, 1, 8)))
        startTime = time.time()
        for i in range(100):
            self.assertEqual(79.05, quoter.getPrice(datetime.date(2007, 1, 8)))
        endTime = time.time() - startTime
        self.assertTrue(endTime < 2)

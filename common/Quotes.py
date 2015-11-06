import unittest
import re
import datetime
import urllib


class YahooQuoter(object):
    def __init__(self, fullYahooSymbol, caching=True):
        self.symbol = fullYahooSymbol
        self.cache = {}
        self.caching = caching

    def getCurrentPrice(self):
        date_to_check = datetime.datetime.utcnow()
        url = 'http://quote.yahoo.com/d/quotes.csv?%s'
        query = {
            's': self.symbol,
            'f': "nl1d1t1",
        }
        params = urllib.urlencode(query)

        # Fetch from Yahoo
        full_url = url % (params,)
        fp = urllib.urlopen(full_url)
        lines = fp.readlines()
        fp.close()

        if len(lines) >= 1:
            line_array = lines[0].split(',')
            theDate = line_array[2]
            pattern = re.compile(r"""(?P<month>\d{1,2}) # month
                                     /
                                     (?P<day>\d{1,2})   # day
                                     /
                                     (?P<year>\d{4,4})  # year
                                     """
                                     , re.VERBOSE)
            match = pattern.search(theDate)
            if match:
                assert int(match.group('year')) == date_to_check.year, "int(match.group('year'))=" + str(int(match.group('year'))) + ' but date_to_check.year=' + date_to_check.year
                assert int(match.group('month')) == date_to_check.month, "int(match.group('month'))=" + str(int(match.group('month'))) + ' but date_to_check.month=' + str(date_to_check.month)
                assert int(match.group('day')) == date_to_check.day, "int(match.group('day'))=" + str(int(match.group('day'))) + ' but date_to_check.day' + str(date_to_check.day)
                value = float(line_array[1])
            else:
                raise Exception("Failed to get current price of %s" % (self.symbol))
        else:
            raise Exception("Failed to get current price of %s" % (self.symbol))
        return value

    def getPrice(self, date_to_check):
        date_to_check_orig = date_to_check
        # TODO: Determine symbol with country code
        if self.caching and date_to_check in self.cache:
            value = self.cache[date_to_check]
            return value

        offset = datetime.timedelta(1)
        maxTries = 7
        numTries = 0
        match = False
        while not match and numTries < maxTries:
            # Construct query
            url = 'http://ichart.finance.yahoo.com/table.csv?%s'
            query = {
                's': self.symbol,
                'd': date_to_check.month - 1,
                'e': date_to_check.day,
                'f': date_to_check.year,
                'a': date_to_check.month - 1,
                'b': date_to_check.day,
                'c': date_to_check.year,
            }
            params = urllib.urlencode(query)

            # Fetch from Yahoo
            full_url = url % (params,)
            fp = urllib.urlopen(full_url)
            lines = fp.readlines()
            fp.close()

            # Parse and check if we got a valid quote or a 404
            if len(lines) > 1:
                line_array = lines[1].split(',')
                pattern = re.compile(r"(?P<year>\d{4,4})\-(?P<month>\d{2,2})\-(?P<day>\d{2,2})")
                match = pattern.match(line_array[0])
                if match:
                    assert int(match.group('year')) == date_to_check.year, "int(match.group('year'))=" + str(int(match.group('year'))) + ' but date_to_check.year=' + date_to_check.year
                    assert int(match.group('month')) == date_to_check.month, "int(match.group('month'))=" + str(int(match.group('month'))) + ' but date_to_check.month=' + str(date_to_check.month)
                    assert int(match.group('day')) == date_to_check.day, "int(match.group('day'))=" + str(int(match.group('day'))) + ' but date_to_check.day' + str(date_to_check.day)
                    value = line_array[4]
                    value = round(float(value), 2)

            # Go backwards in time one more day
            date_to_check -= offset

            numTries += 1

        if numTries == maxTries:
            raise Exception('No quote found')
        else:
            if self.caching:
                self.cache[date_to_check_orig] = value
            return value


class TestQuotes(unittest.TestCase):
    def testExchangeRates(self):
        quoter = YahooQuoter('USDCAD=X')
        price = quoter.getCurrentPrice()
        assert 0.5 < price < 1.6

    def testGetTSXQuote(self):
        quoter = YahooQuoter('xic.TO', caching=True)
        self.assertEquals(81.30, quoter.getPrice(datetime.date(2006, 12, 29)))
        self.assertEquals(81.30, quoter.getPrice(datetime.date(2006, 12, 30)))
        self.assertEquals(81.30, quoter.getPrice(datetime.date(2006, 12, 31)))
        self.assertEquals(81.30, quoter.getPrice(datetime.date(2007, 1, 1)))
        self.assertEquals(81.51, quoter.getPrice(datetime.date(2007, 1, 2)))
        self.assertEquals(80.11, quoter.getPrice(datetime.date(2007, 1, 3)))
        self.assertEquals(78.98, quoter.getPrice(datetime.date(2007, 1, 4)))
        self.assertEquals(78.60, quoter.getPrice(datetime.date(2007, 1, 5)))
        self.assertEquals(79.05, quoter.getPrice(datetime.date(2007, 1, 8)))
        self.assertEquals(14.09, quoter.getPrice(datetime.date(2009, 1, 1)))

    def testCache(self):
        """
        Test caching feature. Make sure that it is working by measuring speed
        """
        import time
        quoter = YahooQuoter('xic.TO', caching=True)
        self.assertEquals(79.05, quoter.getPrice(datetime.date(2007, 1, 8)))
        startTime = time.time()
        for i in xrange(100):
            self.assertEquals(79.05, quoter.getPrice(datetime.date(2007, 1, 8)))
        endTime = time.time() - startTime
        self.assertTrue(endTime < 2)


if __name__ == "__main__":
    unittest.main()

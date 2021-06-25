import datetime
from decimal import Decimal, Context

import yfinance

from django.core.management import BaseCommand

from portfolio.models import Stock, Price


class Command(BaseCommand):
    help = "Updates all prices"

    def handle(self, **kwargs):
        for stock in Stock.objects.all():
            self.stdout.write("Fetching price for {}".format(stock))
            today = datetime.date.today()
            if Price.objects.filter(date=today, stock=stock).exists():
                self.stdout.write("Already have a price for today")
                price = Price.objects.get(date=today, stock=stock)
            else:
                price = Price(stock=stock, date=today)
            self._update_price(stock, price)

    def _update_price(self, stock, price):
        symbol = stock.symbol.replace(".", "-")
        if stock.exchange == Stock.Exchange.TSX:
            symbol = symbol + ".TO"
        else:
            self.stderr.write(
                "Symbol: {}. We don't handle this exchange yet: {}".format(
                    stock.symbol, stock.exchange
                )
            )
            return
        self.stdout.write("Looking up symbol {}".format(symbol))
        new_price = round(
            Decimal(
                yfinance.Ticker(symbol).info["regularMarketPrice"],
                context=Context(prec=120),
            ),
            4,
        )
        if new_price != price.price:
            self.stdout.write(
                "Updating price from {} to {}".format(price.price, new_price)
            )
            price.price = new_price
            price.save()
        else:
            self.stdout.write("No update required")

import datetime
from decimal import Decimal, Context

import yfinance

from django.core.management import BaseCommand

from common import xirr
from portfolio.models import Stock, Price, Position, Transaction


class Command(BaseCommand):
    help = "Calculates XIRR"

    def handle(self, **kwargs):
        today = datetime.date.today()
        for position in Position.objects.all():
            if not position.stock.exchange:
                continue
            self.stdout.write("Updating XIRR for {}".format(position))
            stock = position.stock
            transactions = Transaction.objects.filter(
                stock=stock, account=position.account
            )
            cash_flows = []
            dates = []
            for transaction in transactions:
                cash_flows.append(float(transaction.cash_flow))
                dates.append(transaction.date)
            # Today's current valuation
            today_price = Price.objects.get(date=today, stock=stock).price
            number_of_shares = position.balance
            today_valuation = today_price * number_of_shares
            cash_flows.append(-float(today_valuation))
            dates.append(today)
            position.xirr = xirr.xirr(cash_flows, dates)
            self.stdout.write("Got XIRR of {}".format(position.xirr))
            position.save()

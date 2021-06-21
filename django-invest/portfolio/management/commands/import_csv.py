import datetime
import os
import csv
from decimal import Decimal

from django.db import transaction
from django.core.management.base import BaseCommand
from portfolio.models import Stock, Transaction, Account, Position


class Command(BaseCommand):
    help = "Imports a CSV file of transactions"

    def add_arguments(self, parser):
        parser.add_argument("csv_file")
        parser.add_argument("account_name")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        account_name = options["account_name"]
        account, _ = Account.objects.get_or_create(name=account_name)
        self.stdout.write(csv_file)
        full_path = os.path.normpath(os.path.join(os.getcwd(), csv_file))
        self.stdout.write(full_path)

        with open(full_path) as f:
            lines = f.readlines()
        if lines[2].startswith("---------"):
            with open(full_path, "w") as f:
                f.write(lines[1])
                f.writelines(lines[3:])
        stocks = {stock.symbol: stock for stock in Stock.objects.all()}
        with open(full_path, newline="") as csvfile, transaction.atomic():
            Transaction.objects.all().delete()
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                # {'Transaction Date': '2020-09-22', 'Settlement Date': '2020-09-22', 'Activity Description': 'Deposit',
                #  'Description': 'BP#0010218625 PAYMENT RECEIVED', 'Symbol': '', 'Quantity': '', 'Price': '',
                #  'Currency': 'CAD', 'Total Amount': '15000.00'}
                transaction_ = Transaction()
                transaction_.account = account
                transaction_.date = parse_date(row["Transaction Date"])
                transaction_.settlement_date = parse_date(row["Settlement Date"])
                transaction_.type = parse_type(row["Activity Description"])
                transaction_.description = row["Description"]
                if row["Symbol"]:
                    if row["Symbol"] in stocks:
                        transaction_.stock = stocks[row["Symbol"]]
                    else:
                        stock = Stock()
                        stock.symbol = row["Symbol"]
                        stock.name = ""
                        stock.quote_symbol = ""
                        stock.save()
                        stocks[stock.symbol] = stock
                        transaction_.stock = stock
                if row["Quantity"]:
                    transaction_.number_of_shares = Decimal(row["Quantity"])
                if row["Price"]:
                    transaction_.price = Decimal(row["Price"])
                transaction_.amount = Decimal(row["Total Amount"])
                transaction_.save()

            # We don't handle cash balances well!
            # Update balances of all positions
            for stock in Stock.objects.filter(transactions__account=account).distinct():
                position = Position()
                position.stock = stock
                position.account = account
                position.balance = sum(
                    [
                        tr.number_of_shares
                        for tr in stock.transactions.filter(
                            account=account,
                            # TODO: This is a bit hacky
                            type__in=(
                                Transaction.TransactionType.BUY,
                                Transaction.TransactionType.SELL,
                            ),
                        )
                    ]
                )
                position.save()


def parse_type(type_string: str) -> Transaction.TransactionType:
    return {
        "Buy": Transaction.TransactionType.BUY,
        "Sell": Transaction.TransactionType.SELL,
        "Dividend": Transaction.TransactionType.DIVIDEND,
        "Interest": Transaction.TransactionType.INTEREST,
        "Deposit": Transaction.TransactionType.DEPOSIT,
        "Non resident tax": Transaction.TransactionType.NON_RESIDENT_TAX,
    }[type_string]


def parse_date(date_string: str) -> datetime.date:
    """
    date_string is a string like "2020-09-22"
    """
    date_split = [int(piece) for piece in date_string.split("-")]
    return datetime.date(*date_split)

from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.


class Account(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    """
    A stock like XIC, VTI
    """

    class Exchange(models.TextChoices):
        TSX = "TSX", _("Toronto Stock Exchange")
        NYSE = "NYSE", _("New York Stock Exchange")
        NASDAQ = "NASDAQ", _("Nasdaq")

    symbol = models.CharField(max_length=20)
    exchange = models.CharField(max_length=20, choices=Exchange.choices)
    name = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return str("{0}".format(self.symbol))

    class Meta:
        ordering = ("symbol",)
        constraints = [
            models.UniqueConstraint(
                fields=["symbol", "exchange"], name="unique_symbol_exchange"
            )
        ]


class Price(models.Model):
    stock = models.ForeignKey("Stock", on_delete=models.PROTECT, unique_for_date="date")
    date = models.DateField()
    price = models.DecimalField(max_digits=12, decimal_places=4)

    def __str__(self):
        return f"{self.date} {self.stock} {self.price}"


class Position(models.Model):
    stock = models.ForeignKey("Stock", on_delete=models.PROTECT)
    account = models.ForeignKey("Account", on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    xirr = models.DecimalField(
        max_digits=12, decimal_places=2, default=None, null=True, blank=True
    )

    def __str__(self):
        return f"{self.account}: {self.stock}: {self.balance} shares"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["stock", "account"], name="unique_stock_account"
            )
        ]


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = "DEP", _("Deposit")
        BUY = "BUY", _("Buy")
        SELL = "SEL", _("Sell")
        DIVIDEND = "DIV", _("Dividend")
        INTEREST = "INT", _("Interest")
        WITHDRAWAL = "WIT", _("Withdrawal")
        NON_RESIDENT_TAX = "NRT", _("Non resident tax")

    account = models.ForeignKey("Account", on_delete=models.PROTECT)
    date = models.DateField()
    settlement_date = models.DateField()
    type = models.CharField(max_length=20, choices=TransactionType.choices)
    stock = models.ForeignKey(
        "Stock",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="transactions",
    )
    price = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    number_of_shares = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    commission = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    dividend_per_share = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    description = models.CharField(max_length=100, blank=True, default="")
    cash_flow = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    original_transaction_row = models.CharField(max_length=200, unique=True)

    def __str__(self):
        ret = f"{self.date} {Transaction.TransactionType(self.type).label}"
        if self.type == Transaction.TransactionType.BUY:
            ret += (
                f" {self.stock}: {self.number_of_shares} @ {self.price} = {self.amount}"
            )
        elif self.type == Transaction.TransactionType.SELL:
            ret += (
                f" {self.stock}: {self.number_of_shares} @ {self.price} = {self.amount}"
            )
        elif self.type == Transaction.TransactionType.DEPOSIT:
            ret += f" {self.amount}"
        elif self.type == Transaction.TransactionType.WITHDRAWAL:
            ret += f" {self.amount}"
        elif self.type == Transaction.TransactionType.DIVIDEND:
            ret += f" {self.stock}: {self.amount}"
        elif self.type == Transaction.TransactionType.INTEREST:
            ret += f" {self.stock}: {self.amount}"
        return ret

    class Meta:
        ordering = ("-date",)

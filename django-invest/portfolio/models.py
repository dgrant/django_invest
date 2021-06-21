from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.


class Account(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Stock(models.Model):
    """
    A stock like XIC, VTI
    """

    symbol = models.CharField(max_length=20, unique=True)
    quote_symbol = models.CharField(max_length=20, blank=True, default="")
    name = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return str("{0}".format(self.symbol))

    class Meta:
        ordering = ("symbol",)


class Position(models.Model):
    stock = models.ForeignKey("Stock", on_delete=models.PROTECT)
    account = models.ForeignKey("Account", on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.account}: {self.stock}: {self.balance} shares"


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
    stock = models.ForeignKey("Stock", on_delete=models.PROTECT, null=True, blank=True, related_name="transactions")
    price = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    number_of_shares = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    commission = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    dividend_per_share = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    description = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        ret = f"{self.date} {Transaction.TransactionType(self.type).label}"
        if self.type == Transaction.TransactionType.BUY:
            ret += f" {self.stock}: {self.number_of_shares} @ {self.price} = {self.amount}"
        elif self.type == Transaction.TransactionType.SELL:
            ret += f" {self.stock}: {self.number_of_shares} @ {self.price} = {self.amount}"
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
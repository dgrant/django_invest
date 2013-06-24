from django.db import models
from django.core.urlresolvers import reverse
import datetime
import Quotes
import xirr

from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.ForeignKey(User, editable=False)
    class Meta:
        abstract = True

#Initially, assume just one currency
#TODO: add multiple currency support
#    -balance calculations

# Create your models here.
class Symbol(UserData):
    """
    This is like a currency. It's a unit of something.
    Examples: USD, CAD, XIC, BNS, TRP, GOOG
    """
    name = models.CharField(max_length=20)
    quote_symbol = models.ForeignKey("Symbol", related_name="related_quote_symbol")
    longname = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode("{0} ({1})".format(self.longname, self.name))

    class Meta:
        verbose_name = "symbol/currency"
        verbose_name_plural = "symbols/currencies"

class Holding(UserData):
    """
    This is something that you accumulate a particular Symbol in.
    It contains a certain amount of one and only one Symbol.
    Multiple Holdings may contain the same Symbol
    """
    name = models.CharField(max_length=100)
    symbol = models.ForeignKey("Symbol")
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    iscash = models.BooleanField()

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('holding_detail', args=[str(self.id)])

    def update_balance(self):
        self.balance = sum(tr.shares for tr in self.transaction_set_to.all())
        self.save()

        # Update returns
        # TODO: need an outer loop that loops over the periods
        ret = Return.objects.filter(holding__id=self.id)
        if len(ret) == 0:
            ret = Return()
        else:
            ret = ret[0]
        ret.holding = self
        ret.period = Return.PERIOD_all
        ret.irr = str(self.get_annualized_return(datetime.datetime(1, 1, 1),
            datetime.date.today())*100)
        ret.save()

    def get_annualized_return(self, start_date, end_date):
        print "get_annualized_return()"
        trs = self.transaction_set_to.filter(
                                    date__gte = start_date
                                    ).filter(date__lte = end_date).order_by("date")

        print "Creating yahoo quoter with", str(self.symbol.name)
        quoter = Quotes.YahooQuoter(str(self.symbol.name))
        # TODO: hard-coded CAD here
        exchange_rate = Quotes.YahooQuoter(str(self.symbol.quote_symbol.name)+"CAD"+"=X").getCurrentPrice() if self.symbol.quote_symbol.name != "CAD" else 1.

        dates = []
        cash_flows = []

        for tr in trs:
            dates.append(tr.date)
            if tr.type == Transaction.DIVIDEND_CASH:
                cash_flows.append(-float(tr.amount))
            else:
                cash_flows.append(float(tr.amount))

        #Get current balance
        dates += [datetime.date.today()]
        print "Calling getPrice with datetime.date.today())"
        cash_flows += [-quoter.getPrice(datetime.date.today()) * exchange_rate * float(self.balance)]
        print "dates=\n", dates
        print "cash flows=\n", cash_flows
        ret = xirr.xirr(cash_flows, dates, 0.)
        print "ret=", ret

        return ret

class Return(UserData):
    PERIOD_all = 0
    PERIOD_1mo = 1
    PERIOD_1yr = 2
    PERIOD_2yr = 3
    PERIOD_3yr = 4
    PERIOD_5yr = 5
    PERIOD_10yr = 6
    PERIOD_15yr = 7

    PERIOD_CHOICES = (
                      (PERIOD_all, "all time"),
                     )
    holding = models.ForeignKey("Holding")
    period = models.IntegerField(choices=PERIOD_CHOICES)
    irr =  models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ("holding",)
        verbose_name = "Annualized Return"

    def __unicode__(self):
        return unicode(self.period)+": "+unicode(self.irr*100)+"%"

class Transaction(UserData):
    BUY_TYPE = 0
    SELL_TYPE = 1
    DIVIDEND_CASH = 2
    STOCK_SPLIT = 3
    TRANSACTION_CHOICES = (
                           (BUY_TYPE, "Buy"),
                           (SELL_TYPE, "Sell"),
                           (DIVIDEND_CASH, "Dividend"),
                           (STOCK_SPLIT, "Stock Split"),
                           )

    to_holding = models.ForeignKey("Holding", null=True, related_name="transaction_set_to")
    from_holding = models.ForeignKey("Holding", null=True, related_name="transaction_set_from")
    type = models.IntegerField(choices=TRANSACTION_CHOICES)
    date = models.DateField()
    shares = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=4, default=1.)
    commission = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    convAmount = models.DecimalField(max_digits=12, decimal_places=2, default=0.)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.)
    notes = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ("-date", "notes",)
        get_latest_by = "date"

    def save(self, *args, **kwargs):
        if self.type in (Transaction.BUY_TYPE, Transaction.SELL_TYPE):
            #change amount to be calculated based on the other fields
            self.convAmount = (self.shares * self.price + self.commission)
            self.amount = self.convAmount * self.exchange_rate
        elif self.type in (Transaction.DIVIDEND_CASH,):
            self.shares = 0.
            self.price = 0.
            self.commission = 0.
            if self.convAmount == 0:
                self.convAmount = self.amount / self.exchange_rate
            elif self.amount == 0:
                self.amount = self.convAmount * self.exchange_rate
            else:
                assert self.amount == self.convAmount * self.exchange_rate
        #call actual save method
        super(Transaction, self).save(*args, **kwargs)

        #update the associated holding with new information
        self.to_holding.update_balance()

    def __unicode__(self):
        buf = []
        buf.append(self.date)
        buf.append(self.TRANSACTION_CHOICES[self.type][1])
        buf.append(self.shares)
        buf.append(u"shares")
        buf.append(u"of")
        buf.append(self.to_holding)
        buf.append(u"@" + unicode(self.price))
        buf.append(u"=")
        buf.append(self.amount)
        buf.append(u"from " + unicode(self.from_holding))
        return u" ".join((unicode(s) for s in buf))

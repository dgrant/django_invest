from django.db import models
from django.core.urlresolvers import reverse
import datetime
from common import Quotes, xirr

from django.contrib.auth.models import User

#Initially, assume just one currency
#TODO: add multiple currency support
#    -balance calculations

class UserData(models.Model):
    user = models.ForeignKey(User, editable=False)
    class Meta:
        abstract = True

class Currency(models.Model):
    """
    A currency like CAD, USD, etc...
    """
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode('{0} ({1})'.format(self.name, self.symbol))

    class Meta:
        verbose_name_plural = 'currencies'

class Exchange(models.Model):
    name = models.CharField(max_length=80)
    currency = models.ForeignKey('Currency')

    def __unicode__(self):
        return unicode('{0}'.format(self.name))

class Stock(models.Model):
    """
    A stock like XIC, VTI
    """
    symbol = models.CharField(max_length=20)
    quote_symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    exchange = models.ForeignKey('Exchange')

    def __unicode__(self):
        return unicode("{0}".format(self.symbol))

class Account(UserData):
    """
    This is an account like "David's RRSP"
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return unicode("{0}".format(self.name))

class Position(UserData):
    """
    """
    stock = models.ForeignKey("Stock")
    account = models.ForeignKey("Account")
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ("account", "stock", 'balance',)

    def __unicode__(self):
        return str(self.stock)

    def get_absolute_url(self):
        return reverse('holding_detail', args=[str(self.id)])

    def update_balance(self):
        self.balance = sum(tr.shares for tr in self.transaction_set_to.all())
        self.save()

        if self.iscash:
            return

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


class Trade(UserData):
    BUY_TYPE = 0
    SELL_TYPE = 1
    TRANSACTION_CHOICES = (
                           (BUY_TYPE, "Buy"),
                           (SELL_TYPE, "Sell"),
                           )
    account = models.ForeignKey("Account")
    stock = models.ForeignKey("Stock")
    type = models.IntegerField(choices=TRANSACTION_CHOICES)
    date = models.DateField()
    number_of_shares = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=3)
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=4, default=1., null=True, blank=True)
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
    position = models.ForeignKey("Position")
    period = models.IntegerField(choices=PERIOD_CHOICES)
    irr =  models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ("position",)
        verbose_name = "Annualized Return"

    def __unicode__(self):
        return unicode(self.period)+": "+unicode(self.irr*100)+"%"



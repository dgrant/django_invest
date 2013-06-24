import django_tables2 as tables
from django_tables2.utils import A

table_class = 'table table-bordered table-hover'

class HoldingsTable(tables.Table):
    name = tables.LinkColumn('holding_detail', args=[A('pk')])
    symbol = tables.Column()
    balance = tables.Column()

    class Meta:
        attrs = {'class': table_class}

class TransactionsTable(tables.Table):
    date = tables.Column()
    type = tables.Column()
    to_holding = tables.Column()
    from_holding = tables.Column()
    shares = tables.Column()
    amount = tables.Column()
    price = tables.Column()
    exchange_rate = tables.Column()
    commission = tables.Column()
    notes = tables.Column()

    class Meta:
        attrs = {'class': table_class}
        order_by = ('date',)

    def render_amount(self, record):
        transaction = record
        return "{0} ${1}".format(transaction.from_holding.symbol, transaction.amount)

    def render_price(self, record):
        transaction = record
        return "{0} ${1} per share".format(transaction.to_holding.symbol.quote_symbol.name, transaction.price)

    def render_commission(self, record):
        transaction = record
        return "{0} ${1}".format(transaction.to_holding.symbol.quote_symbol.name, transaction.commission)

    def render_exchange_rate(self, record):
        transaction = record
        if transaction.to_holding.symbol.quote_symbol == transaction.from_holding.symbol:
            return ""
        else:
            return "${0} {1} / ${2} 1.0".format(transaction.from_holding.symbol.name, transaction.exchange_rate, transaction.to_holding.symbol.quote_symbol.name)

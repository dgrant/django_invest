from portfolio.models import Holding, Return, Symbol, Transaction 
from django.contrib import admin

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 5
    fk_name = "to_holding"

class HoldingAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'balance', )
    inlines = (TransactionInline,)

class SymbolAdmin(admin.ModelAdmin):
    list_display = ('name', 'longname', 'quote_symbol', )

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('to_holding', 'from_holding', 'type', 'date', 'shares', 'price', 'commission', 'convAmount', 'exchange_rate', 'amount',)
    list_filter = ('to_holding', 'from_holding', 'date',)

class ReturnAdmin(admin.ModelAdmin):
    list_display = ('holding', 'period', 'irr',)
    list_filter = ('holding',)

admin.site.register(Holding, HoldingAdmin)
admin.site.register(Symbol, SymbolAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Return, ReturnAdmin)

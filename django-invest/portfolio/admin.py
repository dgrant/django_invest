from django.contrib import admin
from portfolio.models import Stock, Transaction, Account, Position


class TransactionInlineAdmin(admin.TabularInline):
    model = Transaction
    readonly_fields = ["date", "settlement_date", "type", "stock", "number_of_shares", "price", "commission", "dividend_per_share", "amount", "description"]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = [TransactionInlineAdmin]

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ["stock"]
    list_display = ["date", "settlement_date", "type", "stock", "number_of_shares", "price", "commission", "dividend_per_share", "amount", "description"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_filter = ["stock", "account"]
    list_display = ["stock", "account", "balance"]
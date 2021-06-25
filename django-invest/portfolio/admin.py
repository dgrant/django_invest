from django.contrib import admin
from portfolio.models import Stock, Transaction, Account, Position, Price


class TransactionInlineAdmin(admin.TabularInline):
    model = Transaction
    readonly_fields = [
        "date",
        "settlement_date",
        "type",
        "stock",
        "number_of_shares",
        "price",
        "commission",
        "dividend_per_share",
        "amount",
        "description",
    ]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = [TransactionInlineAdmin]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["symbol", "exchange", "name"]
    list_filter = ["exchange"]


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_filter = ["date", "stock"]
    list_display = ["date", "stock", "price"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ["stock"]
    list_display = [
        "date",
        "settlement_date",
        "type",
        "stock",
        "number_of_shares",
        "price",
        "commission",
        "dividend_per_share",
        "amount",
        "cash_flow",
        "description",
    ]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_filter = ["stock", "account"]
    list_display = ["stock", "stock_name", "account", "balance", "get_xirr"]

    @admin.display(description='XIRR', ordering="xirr")
    def get_xirr(self, obj):
        if obj.xirr:
            return f"{(obj.xirr * 100):.{1}f}%"
        else:
            ""

    @admin.display(description="Stock Name")
    def stock_name(self, position):
        return f"{position.stock.name}"

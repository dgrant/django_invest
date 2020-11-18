from .models import *
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    exclude = ("user",)

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(UserAdmin, self).has_change_permission(
            request, obj
        )
        if not has_class_permission:
            return False
        if (
            obj is not None
            and not request.user.is_superuser
            and request.user.id != obj.user.id
        ):
            return False
        return True

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()


# class TradeInline(admin.TabularInline):
#    model = Trade
#    extra = 5
#    fk_name = "


class PositionAdmin(UserAdmin, admin.ModelAdmin):
    #    pass
    list_display = (
        "stock",
        "account",
        "balance",
    )


#    inlines = (TradeInline,)


class StockAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "name",
        "quote_symbol",
        "exchange",
    )


class TradeAdmin(UserAdmin, admin.ModelAdmin):
    pass


#    list_display = ('to_holding', 'from_holding', 'type', 'date', 'shares', 'price', 'commission', 'convAmount', 'exchange_rate', 'amount',)
#    list_filter = ('to_holding', 'from_holding', 'date',)


class ReturnAdmin(UserAdmin, admin.ModelAdmin):
    pass


#    list_display = ('holding', 'period', 'irr',)
#    list_filter = ('holding',)


admin.site.register(Position, PositionAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Trade, TradeAdmin)
admin.site.register(Return, ReturnAdmin)
admin.site.register(Exchange)
admin.site.register(Currency)
admin.site.register(Account)

from django.contrib import admin
from . import models


class BrokerAdmin(admin.ModelAdmin):
    list_display = ('broker_title',)


class BrokerReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'broker', 'report', 'uploaded')


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency_ticker', 'currency_rus')


class DealAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'transaction_type', 'ticker', 'price', 'currency', 'quantity',
                    'total_cost', )
    list_filter = ('user', 'date', 'transaction_type', 'ticker', )


class ReplenishmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'currency', 'count')


class PortfolioStateRowAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticker', 'state', 'quantity', 'average_buy_price', 'average_sell_price', )
    list_filter = ('user', 'ticker', 'state')


admin.site.register(models.Broker, BrokerAdmin)
admin.site.register(models.BrokerReport, BrokerReportAdmin)
admin.site.register(models.Currency, CurrencyAdmin)
admin.site.register(models.Deal, DealAdmin)
admin.site.register(models.Replenishment, ReplenishmentAdmin)
admin.site.register(models.PortfolioStateRow, PortfolioStateRowAdmin)

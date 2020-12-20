from django.contrib import admin
from . import models


class BrokerAdmin(admin.ModelAdmin):
    list_display = ('broker_title',)


class BrokerReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'broker', 'report', 'uploaded_at')


class SectorAdmin(admin.ModelAdmin):
    list_display = ('sector_title', 'sector_rus')


class IndustryAdmin(admin.ModelAdmin):
    list_display = ('industry_title', 'industry_rus', 'sector')


class StockAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'ticker_yf', 'name', 'currency', 'sector', 'industry', 'logo')


class StockPriceAdmin(admin.ModelAdmin):
    list_display = ('date', 'ticker', 'open', 'high', 'low', 'close', 'volume')
    list_filter = ('date', 'ticker')
    search_fields = ('date', 'ticker')


class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('tt_title', )


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency_ticker', 'currency_rus')


class DealAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'transaction_type', 'ticker', 'price', 'currency', 'quantity',
                    'cost_without_nkd', 'nkd', 'total_cost', 'fee')
    list_filter = ('user', 'date', 'time', 'transaction_type', 'ticker', 'total_cost',)


admin.site.register(models.Broker, BrokerAdmin)
admin.site.register(models.BrokerReport, BrokerReportAdmin)
admin.site.register(models.Stock, StockAdmin)
admin.site.register(models.StockPrice, StockPriceAdmin)
admin.site.register(models.Sector, SectorAdmin)
admin.site.register(models.Industry, IndustryAdmin)
admin.site.register(models.TransactionType, TransactionTypeAdmin)
admin.site.register(models.Currency, CurrencyAdmin)
admin.site.register(models.Deal, DealAdmin)

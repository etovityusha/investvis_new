from django.contrib import admin
from . import models


class BrokerAdmin(admin.ModelAdmin):
    list_display = ('broker_title',)


class BrokerReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'broker', 'report', 'uploaded_at')


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
admin.site.register(models.TransactionType, TransactionTypeAdmin)
admin.site.register(models.Currency, CurrencyAdmin)
admin.site.register(models.Deal, DealAdmin)

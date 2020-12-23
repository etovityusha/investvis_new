from django.contrib import admin
from . import models


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


admin.site.register(models.StockPrice, StockPriceAdmin)
admin.site.register(models.Sector, SectorAdmin)
admin.site.register(models.Industry, IndustryAdmin)
admin.site.register(models.Stock, StockAdmin)
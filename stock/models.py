from django.db import models


class Sector(models.Model):
    sector_title = models.CharField(max_length=50, unique=True, verbose_name='Сектор')
    sector_rus = models.CharField(max_length=50, default='', verbose_name='Сектор ru')

    class Meta:
        verbose_name = 'Сектор'
        verbose_name_plural = 'Сектора'
        ordering = ['sector_title']

    def __str__(self):
        return self.sector_rus


class Industry(models.Model):
    industry_title = models.CharField(max_length=100, verbose_name='Индустрия')
    industry_rus = models.CharField(max_length=100, verbose_name='Индустрия ru', blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Индустрия'
        verbose_name_plural = 'Индустрии'
        ordering = ['industry_title']

    def __str__(self):
        return self.industry_title


class Currency(models.Model):
    currency_ticker = models.CharField(max_length=6, unique=True, verbose_name='Идентификатор')
    currency_rus = models.CharField(max_length=150, verbose_name='Название')

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
        ordering = ['currency_ticker']

    def __str__(self):
        return self.currency_ticker


class Stock(models.Model):
    ticker = models.CharField(max_length=50, db_index=True, unique=True, verbose_name='Индентификатор')
    ticker_yf = models.CharField(max_length=50, db_index=True, unique=True,
                                 verbose_name='Индентификатор для Yahoo Finance', null=True)
    name = models.CharField(max_length=200, verbose_name='Название', null=True, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, verbose_name='Сектор', null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT, verbose_name='Индустрия', null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name='Валюта', null=True, blank=True)
    logo = models.ImageField(verbose_name='Логотип', blank=True, null=True, default=None, upload_to='documents/logos')
    decimal_places = models.IntegerField(verbose_name='Десятичные знаки', default=2)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
        ordering = ['ticker']

    def __str__(self):
        return self.ticker


class StockPrice(models.Model):
    date = models.DateField(db_index=True, verbose_name='Дата')
    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='Индентификатор')
    open = models.DecimalField(verbose_name='Цена открытия', max_digits=19, decimal_places=6)
    high = models.DecimalField(verbose_name='Максимальная цена', max_digits=19, decimal_places=6)
    low = models.DecimalField(verbose_name='Минимальная цена', max_digits=19, decimal_places=6)
    close = models.DecimalField(verbose_name='Цена закрытия', max_digits=19, decimal_places=6)
    volume = models.IntegerField(verbose_name='Объём торгов')

    def as_list_for_graph(self):
        return [self.date, self.close]

    class Meta:
        verbose_name = 'Котировка'
        verbose_name_plural = 'Котировки'
        ordering = ['-date', 'ticker']


class CurrencyCourse(models.Model):
    currency1 = models.ForeignKey(Currency, verbose_name='Валюта 1', on_delete=models.CASCADE,
                                  related_name='main_currency')
    currency2 = models.ForeignKey(Currency, verbose_name='Валюта 2', on_delete=models.CASCADE,
                                  related_name='second_currency')
    date = models.DateField(db_index=True, verbose_name='Дата')
    open = models.DecimalField(verbose_name='Цена открытия', max_digits=19, decimal_places=6)
    high = models.DecimalField(verbose_name='Максимальная цена', max_digits=19, decimal_places=6)
    low = models.DecimalField(verbose_name='Минимальная цена', max_digits=19, decimal_places=6)
    close = models.DecimalField(verbose_name='Цена закрытия', max_digits=19, decimal_places=6)

    class Meta:
        verbose_name = 'Курс валют'
        verbose_name_plural = 'Курсы валют'
        ordering = ['-date', 'currency1', 'currency2']

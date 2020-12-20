from django.db import models
from django.contrib.auth.models import User


class Broker(models.Model):
    broker_title = models.CharField(max_length=150, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.broker_title

    class Meta:
        verbose_name = 'Брокер'
        verbose_name_plural = 'Брокеры'
        ordering = ['broker_title']


class BrokerReport(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)
    broker = models.ForeignKey(Broker, on_delete=models.PROTECT,  verbose_name='Брокер', blank=True, null=True)
    report = models.FileField(upload_to="imported_reports/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'
        ordering = ['uploaded_at']


class Sector(models.Model):
    sector_title = models.CharField(max_length=50, unique=True, verbose_name='Сектор')
    sector_rus = models.CharField(max_length=50, default='', verbose_name='Сектор ru')

    class Meta:
        verbose_name = 'Сектор'
        verbose_name_plural = 'Сектора'
        ordering = ['sector_title']

    def __str__(self):
        return self.sector_title


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


class TransactionType(models.Model):
    tt_title = models.CharField(max_length=50, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Торговая операция'
        verbose_name_plural = 'Торговые операции'
        ordering = ['tt_title']

    def __str__(self):
        return self.tt_title


class Stock(models.Model):
    ticker = models.CharField(max_length=50, db_index=True, unique=True, verbose_name='Индентификатор')
    ticker_yf = models.CharField(max_length=50, db_index=True, unique=True,
                                 verbose_name='Индентификатор для Yahoo Finance', null=True)
    name = models.CharField(max_length=200, verbose_name='Название')
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, verbose_name='Сектор')
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT, verbose_name='Индустрия')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name='Валюта')
    logo = models.ImageField(verbose_name='Логотип', blank=True, null=True, default=None, upload_to='documents/logos')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
        ordering = ['ticker']

    def __str__(self):
        return self.ticker


class StockPrice(models.Model):
    date = models.DateField(db_index=True, verbose_name='Дата')
    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='Индентификатор')
    open = models.DecimalField(verbose_name='Цена открытия', max_digits=19, decimal_places=4)
    high = models.DecimalField(verbose_name='Максимальная цена', max_digits=19, decimal_places=4)
    low = models.DecimalField(verbose_name='Минимальная цена', max_digits=19, decimal_places=4)
    close = models.DecimalField(verbose_name='Цена закрытия', max_digits=19, decimal_places=4)
    volume = models.IntegerField(verbose_name='Объём торгов')

    class Meta:
        verbose_name = 'Котировка'
        verbose_name_plural = 'Котировки'
        ordering = ['-date', 'ticker']


class Deal(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, verbose_name='Тип операции')
    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Идентификатор')
    price = models.DecimalField(null=True, blank=True, verbose_name='Цена', max_digits=19, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='Валюта')
    quantity = models.IntegerField(verbose_name='Количество')
    cost_without_nkd = models.DecimalField(null=True, blank=True, verbose_name='Стоимость без НКД', max_digits=19,
                                           decimal_places=2)
    nkd = models.DecimalField(null=True, blank=True, verbose_name='НКД', max_digits=19, decimal_places=2)
    total_cost = models.DecimalField(null=True, blank=True, verbose_name='Общая стоимость', max_digits=19,
                                     decimal_places=2)
    fee = models.DecimalField(null=True, blank=True, verbose_name='Комиссия', max_digits=19, decimal_places=2)

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'
        ordering = ['-date', '-time', 'total_cost']


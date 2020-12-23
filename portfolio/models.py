from django.db import models
from django.contrib.auth.models import User
from stock.models import Stock, Currency


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


class TransactionType(models.Model):
    tt_title = models.CharField(max_length=50, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Торговая операция'
        verbose_name_plural = 'Торговые операции'
        ordering = ['tt_title']

    def __str__(self):
        return self.tt_title


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


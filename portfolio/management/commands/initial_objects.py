from django.core.management.base import BaseCommand

from portfolio import models as pm
from stock import models as sm


class Command(BaseCommand):
    def handle(self, *args, **options):
        pm.Broker.objects.get_or_create(broker_title='Тинькофф')

        for cur, cur_rus in zip(['USD', 'EUR', 'RUB'], ['Доллар', 'Евро', 'Рубль']):
            sm.Currency.objects.get_or_create(currency_ticker=cur, currency_rus=cur_rus)

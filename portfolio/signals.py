from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from portfolio.models import Deal, BrokerReport
from portfolio.services.states import update_portfolio_row_states
from portfolio.services.import_deals.import_main import preprocessing


@receiver(post_delete, sender=Deal)
@receiver(post_save, sender=Deal)
def update_portfolio_row(instance, **kwargs):
    """
    Сигнал, срабатывающий при создании или удалении сделки.
    Обновлет в модели портфеля позиции по акции, с которой было действие.
    """
    update_portfolio_row_states(user=instance.user, stock=instance.ticker)


@receiver(post_save, sender=BrokerReport)
def singal_import_deals_from_brokerreport(instance, sender, **kwargs):
    preprocessing(instance)

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from portfolio.models import Deal
from portfolio.services.states import update_portfolio_row_states


@receiver(post_delete, sender=Deal)
@receiver(post_save, sender=Deal)
def update_portfolio_row(instance, **kwargs):
    """
    Сигнал, срабатывающий при создании или удалении сделки.
    Обновлет в модели портфеля позиции по акции, с которой было действие.
    """
    update_portfolio_row_states(user=instance.user, stock=instance.ticker)

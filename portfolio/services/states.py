from django.contrib.auth.models import User
from portfolio.models import Deal, PortfolioStateRow
from stock.models import Stock

import numpy as np


def update_portfolio_row_states(user: User, stock: Stock):
    """
    Обновляет в модели позиций портфеля статусы по позиции.
    При наличии сделок с проадажами средняя цена покупки рассчитывается
    по правилу FIFO. Read more: https://en.wikipedia.org/wiki/FIFO_and_LIFO_accounting
    """
    deals_buy = Deal.objects.filter(
        user=user,
        ticker=stock,
        transaction_type='B'
    )
    deals_sell = Deal.objects.filter(
        user=user,
        ticker=stock,
        transaction_type='S'
    )
    buys, sells = [], []
    for deal in deals_buy:
        for i in range(deal.quantity):
            buys.append(deal.price)
    for deal in deals_sell:
        for i in range(deal.quantity):
            sells.append(deal.price)

    if sells:
        if len(buys) == len(sells):
            PortfolioStateRow.objects.filter(user=user, ticker=stock, state='O').first().delete()
        number_of_sold = len(sells)
        average_buy = np.mean(buys[:number_of_sold])
        average_sell = np.mean(sells)
        PortfolioStateRow.objects.update_or_create(user=user,
                                                   ticker=stock,
                                                   state='C',
                                                   defaults={
                                                       'quantity': number_of_sold,
                                                       'average_buy_price': average_buy,
                                                       'average_sell_price': average_sell,
                                                   })
    else:
        try:
            PortfolioStateRow.objects.filter(user=user, ticker=stock, state='C').delete()
        except:
            pass

    if len(buys) > len(sells):
        average_buy = np.mean(buys[len(sells):])
        PortfolioStateRow.objects.update_or_create(user=user,
                                                   ticker=stock,
                                                   state='O',
                                                   defaults={
                                                       'quantity': len(buys) - len(sells),
                                                       'average_buy_price': average_buy,
                                                       'average_sell_price': None,
                                                   })

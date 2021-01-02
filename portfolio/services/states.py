from django.contrib.auth.models import User
from portfolio.models import Deal, TransactionType, PortfolioStateRow
from stock.models import Stock

import numpy as np


def update_portfolio_row_states(user_id: int, ticker: str):
    user = User.objects.get(pk=user_id)
    stock = Stock.objects.get(ticker=ticker)
    deals_buy = Deal.objects.filter(user=user,
                                    ticker=stock,
                                    transaction_type=TransactionType.objects.get(tt_title='Покупка'))
    deals_sell = Deal.objects.filter(user=user,
                                     ticker=stock,
                                     transaction_type=TransactionType.objects.get(tt_title='Продажа'))
    buys, sells = [], []
    for deal in deals_buy:
        for i in range(deal.quantity):
            buys.append(deal.price)
    for deal in deals_sell:
        for i in range(deal.quantity):
            sells.append(deal.price)

    if sells:
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
    if buys:
        average_buy = np.mean(buys[len(sells):])
        PortfolioStateRow.objects.update_or_create(user=user,
                                                   ticker=stock,
                                                   state='O',
                                                   defaults={
                                                       'quantity': len(buys) - len(sells),
                                                       'average_buy_price': average_buy,
                                                       'average_sell_price': None,
                                                   })

from django.contrib.auth.models import User
from portfolio.models import Deal, TransactionType, PortfolioStateRow
from stock.models import StockPrice, Stock

import numpy as np
from pandas import date_range
from datetime import datetime


def update_portfolio_row_states_from(user_id: int, ticker: str, date: str) -> None:
    user = User.objects.get(pk=user_id)
    for date in date_range(start=date, end=datetime.today()):
        _update_portfolio_row_state(user, ticker, date)


def _update_portfolio_row_state(user: User, ticker: str, date: str) -> None:
    deals_buy = Deal.objects.filter(user=user,
                                    ticker=Stock.objects.get(ticker=ticker),
                                    date__lte=date,
                                    transaction_type=TransactionType.objects.get(tt_title='Покупка'))
    deals_sell = Deal.objects.filter(user=user,
                                     ticker=Stock.objects.get(ticker=ticker),
                                     date__lte=date,
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
                                                   date=date,
                                                   ticker=Stock.objects.get(ticker=ticker),
                                                   state='C',
                                                   defaults={
                                                       'quantity': number_of_sold,
                                                       'average_buy_price': average_buy,
                                                       'change': (average_sell/average_buy - 1) * 100,
                                                   })
    if buys:
        average_buy = np.mean(buys[len(sells):])
        price = StockPrice.objects.filter(ticker=Stock.objects.get(ticker=ticker), date__lte=date).\
            values_list('close', flat=True)[0]
        PortfolioStateRow.objects.update_or_create(user=user,
                                                   date=date,
                                                   ticker=Stock.objects.get(ticker=ticker),
                                                   state='O',
                                                   defaults={
                                                       'quantity': len(buys)-len(sells),
                                                       'average_buy_price': average_buy,
                                                       'change': (price / average_buy - 1) * 100,
                                                   })

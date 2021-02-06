from django.contrib.auth.models import User

from typing import NamedTuple

from portfolio.models import PortfolioStateRow
from stock.models import StockPrice, Stock


class PortfolioRow(NamedTuple):
    ticker: str
    quantity: int
    cost: float
    currency: str
    current_price: float
    average_buy_price: float
    change: float
    sector: str
    industry: str


def get_open_portfolio_rows_by_user(user: User) -> list:
    """
    Извлекает из таблицы PortfolioStateRow открытые позиции указанного пользователя.
    Возвращает в виде списка.
    """
    portfolio_list = []
    ids, average_buy_prices, quantitys = get_portfolio_rows_info(user=user, state='O')
    for stock_id, abp, q in zip(ids, average_buy_prices, quantitys):
        stock = Stock.objects.get(pk=stock_id)
        current_price = StockPrice.objects.filter(ticker=stock).values_list('close', flat=True)[0]
        portfolio_list.append(PortfolioRow(ticker=stock.ticker,
                                           quantity=q,
                                           cost=current_price * q,
                                           currency=stock.currency,
                                           current_price=current_price,
                                           average_buy_price=abp,
                                           change=current_price/(abp / 100)-100,
                                           sector=stock.sector,
                                           industry=stock.industry))
    return portfolio_list


class PortfolioClosedRow(NamedTuple):
    ticker: str
    average_buy_price: float
    average_sell_price: float
    currency: str
    quantity: int
    income: float
    sector: str
    industry: str


def get_closed_portfolio_rows_by_user(user: User) -> list:
    """
    Извлекает из таблицы PortfolioStateRow закрытые позиции указанного пользователя.
    Возвращает в виде списка.
    """
    portfolio_list = []
    ids, average_buy_prices, average_sell_prices, quantitys = get_portfolio_rows_info(user=user, state='C')
    for stock_id, abp, asp, q in zip(ids, average_buy_prices, average_sell_prices, quantitys):
        stock = Stock.objects.get(pk=stock_id)
        portfolio_list.append(PortfolioClosedRow(ticker=stock.ticker,
                                                 average_buy_price=abp,
                                                 average_sell_price=asp,
                                                 currency=stock.currency,
                                                 quantity=q,
                                                 income=((asp - abp) * q),
                                                 sector=stock.sector,
                                                 industry=stock.industry))
    return portfolio_list


def get_portfolio_rows_info(user: User, state: str) -> tuple:
    ids = PortfolioStateRow.objects.filter(user=user, state=state).values_list('ticker', flat=True)
    average_buy_prices = PortfolioStateRow.objects.filter(user=user, state=state).\
        values_list('average_buy_price', flat=True)
    quantitys = PortfolioStateRow.objects.filter(user=user, state=state).\
        values_list('quantity', flat=True)
    if state == 'C':
        average_sell_prices = PortfolioStateRow.objects.filter(user=user, state=state).\
            values_list('average_sell_price', flat=True)
        return ids, average_buy_prices, average_sell_prices, quantitys
    return ids, average_buy_prices, quantitys

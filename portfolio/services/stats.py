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


def get_open_portfolio_rows_by_user(user: User):
    ids = PortfolioStateRow.objects.filter(user=user, state='O').values_list('ticker', flat=True)
    average_buy_prices = PortfolioStateRow.objects.filter(user=user, state='O').values_list('average_buy_price',
                                                                                            flat=True)
    quantitys = PortfolioStateRow.objects.filter(user=user, state='O').values_list('quantity', flat=True)
    portfolio_list = []
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

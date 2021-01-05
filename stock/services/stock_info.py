from portfolio.models import Deal
from stock.models import Stock, StockPrice
from portfolio.models import PortfolioStateRow

import pandas as pd
import plotly.graph_objects as go


def get_data_about_stock(stock: Stock):
    """
    Извлекает из БД информацию о компании по тикеру.
    """
    return {'ticker': stock,
            'name': stock.name,
            'currency': stock.currency,
            'sector': stock.sector,
            'industry': stock.industry,
            'logo': stock.logo,
            'decimal_places': stock.decimal_places,
            }


def get_stock_quotations(stock: Stock, n: int):
    """
    Извлекает из БД котировки за последние n дней.
    """
    return StockPrice.objects.filter(ticker=stock)[:n]


def get_deals_with_this_stock(stock: Stock, user_id):
    """
    Извлекает из БД сделки, фильтруя по тикеру и id пользоваля.
    """
    return Deal.objects.filter(ticker=stock,
                               user_id=user_id)


def get_open_position(stock: Stock, user_id):
    return PortfolioStateRow.objects.filter(user_id=user_id,
                                            ticker=stock,
                                            state='O')


def get_closed_position(stock: Stock, user_id):
    return PortfolioStateRow.objects.filter(user_id=user_id,
                                            ticker=stock,
                                            state='C')


def get_current_price_and_last_day_change(stock: Stock):
    prices = StockPrice.objects.filter(ticker=stock).values_list('close', flat=True)
    return prices[0], int(((prices[0] / prices[1]) * 100 - 100) * 100) / 100, (prices[0] - prices[1])


def graph(stock: Stock):
    df = pd.DataFrame(list(StockPrice.objects.filter(ticker=stock).values()))
    fig = go.Figure(data=go.Scatter(x=df['date'], y=df['close']))
    fig.update_xaxes(
        rangeslider_visible=True
    )
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="Месяц",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="Полгода",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="Этот год",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="Год",
                         step="year",
                         stepmode="backward"),
                    dict(count=5,
                         label="5 лет",
                         step="year",
                         stepmode="backward"),

                    dict(step="all",
                         label="Всё время")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig.to_html(full_html=False, default_height=700, default_width=900)

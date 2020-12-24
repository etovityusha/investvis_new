import pandas as pd
import yfinance as yf

from typing import NamedTuple

from django.db import connection


class PortfolioRow(NamedTuple):
    ticker: str
    count: int
    cost: float
    currency: str
    current_price: float
    average_buy: float
    change: float
    sector: str
    industry: str


def get_deals_dataframe_for_user(user_id: int, schema='public.') -> pd.DataFrame:
    """Получает на вход идентификатор пользователя. Возвращает ДатаФрейм со всеми его операциями покупок/продажи"""
    query = f"""
        SELECT d.user_id, d.date, d.time, tt.tt_title tt,  s.ticker, d.price, c.currency_ticker currency, d.quantity, 
               d.cost_without_nkd, d.nkd, d.total_cost, d.fee
        FROM {schema}portfolio_deal  d
        INNER JOIN {schema}portfolio_transactiontype tt ON d.transaction_type_id = tt.ID
        INNER JOIN {schema}stock_stock s ON d.ticker_id = s.ID
        INNER JOIN {schema}stock_currency c ON d.currency_id = c.ID
        where d.user_id={user_id}
        ORDER BY date
    """
    deals = pd.read_sql_query(query, connection)
    deals['date'] = pd.to_datetime(deals['date'], format='%Y-%m-%d')
    return deals



def get_stocks_quotes_from_db(stocks_list: list, schema='public.') -> pd.DataFrame:
    stocks_list_for_db_query = _get_stocks_list_string_for_db_query(stocks_list)
    query = f"""
                SELECT  sp.date, sp.close, s.ticker
                FROM {schema}stock_stockprice sp
                INNER JOIN {schema}stock_stock s ON sp.ticker_id = s.ID
                WHERE ticker IN {stocks_list_for_db_query}"""
    return pd.read_sql_query(query, connection)


def get_portfolio_only_stocks(deals, date):
    """
    Получает на вход предобработанные с помощью функции preprocessed excel отчёты.
    Возвращает состояние портфеля акций на указанную дату. Валюта и облигации исключаются.
    """
    dct = {}
    df = deals[deals['date'] <= date]
    dct['USD'] = 0
    for (d, bs, t, q, p, c) in zip(list(df['date']), list(df['tt']), list(df['ticker']),
                                   list(df['quantity']), list(df['total_cost']), list(df['currency'])):
        if bs == 'Покупка':
            if 'USD' in t:
                dct['USD'] += int(q)
            else:
                if t in dct:
                    dct[t] += int(q)
                else:
                    dct[t] = int(q)
        elif bs == 'Продажа':
            if 'USD' in t:
                dct['USD'] -= int(q)
            else:
                dct[t] -= int(q)
    dct['RUB'] = 0
    dct['USD'] = 0
    return {k: v for k, v in dct.items() if v != 0 and len(k) < 6}


def download_currencyes_data():
    usdrub_df = yf.Ticker('RUB=X').history(period="5y").reset_index()
    eurusd_df = yf.Ticker('EURUSD=X').history(period="5y").reset_index()
    eurrub_df = yf.Ticker('EURRUB=X').history(period="5y").reset_index()
    return usdrub_df, eurusd_df, eurrub_df


def get_currency_values_as_of_the_date(date: str, usdrub_df, eurusd_df, eurrub_df) -> tuple:
    usdrub = usdrub_df[usdrub_df['Date'] <= date]['Close'].values[-1]
    eurusd = eurusd_df[eurusd_df['Date'] <= date]['Close'].values[-1]
    eurrub = eurrub_df[eurrub_df['Date'] <= date]['Close'].values[-1]
    return usdrub, eurusd, eurrub


def get_stocks_info_from_db(stocks_list: list, schema='public.') -> pd.DataFrame:
    stocks_list_for_db_query = _get_stocks_list_string_for_db_query(stocks_list)
    query = f"""
                SELECT s.ticker, s.name, c.currency_ticker currency, se.sector_title sector,
                i.industry_title industry
                
                FROM {schema}stock_stock s
                INNER JOIN {schema}stock_currency c ON s.currency_id = c.ID
                INNER JOIN {schema}stock_sector se ON s.sector_id = se.ID
                INNER JOIN {schema}stock_industry i ON s.industry_id = i.ID
                WHERE s.ticker IN {stocks_list_for_db_query}"""
    return pd.read_sql_query(query, connection)


def _get_stocks_list_string_for_db_query(stocks_list: list) -> str:
    """Получает на вход список тикеров. Возвращает строку для конкатинации к запросу в базу данных в параметр IN"""
    stocks_list = ["'" + ticker + "'" for ticker in stocks_list]
    return '(' + ', '.join(stocks_list) + ')'


def get_info_for_portfolio_stats(user_id: int):
    deals = get_deals_dataframe_for_user(user_id=user_id)
    portfolio = get_portfolio_only_stocks(deals, pd.to_datetime('today').strftime("%Y-%m-%d"))
    stocks_list = portfolio.keys()
    quotes = get_stocks_quotes_from_db(stocks_list)
    stocks_info = get_stocks_info_from_db(stocks_list)

    portfolio_list = []
    for ticker, count in portfolio.items():
        df_for_average = deals[(deals['ticker'] == ticker) & (deals['tt'] == 'Покупка') &
                               (deals['date'] <= pd.to_datetime('today').strftime("%Y-%m-%d"))]
        currency = stocks_info[stocks_info['ticker'] == ticker]['currency'].values[0]
        current_price = quotes[quotes['ticker'] == ticker]['close'].values[-1]
        average_buy = sum(df_for_average['total_cost']) / sum(df_for_average['quantity'])
        change = current_price / (average_buy / 100) - 100
        sector = stocks_info[stocks_info['ticker'] == ticker]['sector'].values[0]
        industry = stocks_info[stocks_info['ticker'] == ticker]['industry'].values[0]
        cost = current_price * count
        portfolio_list.append(PortfolioRow(ticker=ticker,
                                           count=count,
                                           cost=cost,
                                           currency=currency,
                                           current_price=current_price,
                                           average_buy=average_buy,
                                           change=change,
                                           sector=sector,
                                           industry=industry))
    return portfolio_list

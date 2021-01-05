from portfolio.services.import_deals import import_tinkoff
from portfolio.models import Deal, TransactionType
from stock.models import Stock, Currency
from stock.services import add_company

import pandas as pd


def preprocessing(instance, **kwargs):
    """
    Обработка импортированного отчёта. Включает в себя:
    1) Добавление в Deals списка сделок и пополнений
    2) Парсинг недостающей информации об акциях:
        > котировки
        > информация (название, сектор, индустрия)
    """
    deals = import_tinkoff.get_deals(instance.report)
    deals['id'] = instance.user
    stocks, bonds, currencies = split_deals_to_categories(deals)
    add_stocks_missing_info_to_db(stocks)
    add_deals_to_db(stocks)


def add_deals_to_db(deals_dataframe):
    """
    Добавляет сделки с акциями, извлеченные из отчета, в базу.
    """
    for deal in deals_dataframe.itertuples():
        try:
            saved = Deal.objects.create(user=deal[8],
                                        date=deal[1],
                                        transaction_type=TransactionType.objects.get(tt_title=deal[2]),
                                        ticker=Stock.objects.get(ticker=deal[3]),
                                        price=deal[4],
                                        currency=Currency.objects.get(currency_ticker=deal[5]),
                                        quantity=deal[6],
                                        total_cost=deal[7]
                                        )
        except Exception as ex:
            print(ex)


def add_stocks_missing_info_to_db(stocks):
    """
    Добавляет отсутсвующую информацию о акциях в БД.
    """
    for ticker in set(stocks['ticker']):
        try:
            Stock.objects.get(ticker=ticker)
        except:
            try:
                obj = Stock.objects.create(ticker=ticker)
                obj.currency = Currency.objects.get(currency_ticker=list(stocks[stocks['ticker'] == ticker]['currency'])[0])
                obj = add_company.download_and_save_stock_data(obj)
                obj.save()
                add_company.download_stock_quotations([obj.ticker_yf])
            except:
                pass


def sum_identical_deals(deals: pd.DataFrame) -> pd.DataFrame:
    """
    Брокер Тинькофф при совершение сделки частями через лимитированную заявку дробит сделки.
    Эта фукнция их объединяет.
    """
    deals[['price', 'quantity', 'total_cost']] = deals[['price', 'quantity', 'total_cost']].astype(float)
    for column_name in ('quantity', 'total_cost', ):
        deals[column_name] = deals.groupby(['date', 'transaction_type', 'ticker', 'price', 'currency'])[column_name].\
            transform('sum')
    return deals.drop_duplicates(subset=['date', 'transaction_type', 'price', 'ticker', 'currency'])


def split_deals_to_categories(df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    """
    Разделение датафрейма со сделками на категории:
        > сделки с акциями
        > сделки с валютой
        > сделки с облигациями
    """
    curs = Currency.objects.all().values_list('currency_ticker', flat=True)
    stocks = df[(df['ticker'].str.len() < 7) & (~df['ticker'].isin(curs))]
    currencies = df[df['ticker'].isin(curs)]
    bonds = df[~df['ticker'].isin(set(list(stocks['ticker']) + list(currencies['ticker'])))]
    return stocks, bonds, currencies

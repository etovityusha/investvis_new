from portfolio.models import Deal
from stock.models import Stock, StockPrice


def get_data_about_stock(stock_ticker: str):
    """
    Извлекает из БД информацию о компании по тикеру.
    """
    obj = Stock.objects.get(ticker=stock_ticker)
    return {'ticker': stock_ticker,
            'name': obj.name,
            'currency': obj.currency,
            'sector': obj.sector,
            'industry': obj.industry,
            'logo': obj.logo}


def get_stock_quotations(stock_ticker: str, n: int):
    """
    Извлекает из БД котировки за последние n дней.
    """
    return StockPrice.objects.filter(ticker=Stock.objects.get(ticker=stock_ticker).id)[:n]


def get_deals_with_this_stock(stock_ticker, user_id):
    """
    Извлекает из БД сделки, фильтруя по тикеру и id пользоваля.
    """
    return Deal.objects.filter(ticker=Stock.objects.get(ticker=stock_ticker).id,
                                      user_id=user_id)
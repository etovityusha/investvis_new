from stock.models import Stock, StockPrice, Currency, CurrencyCourse

import yfinance as yf
from celery import shared_task


@shared_task
def update_currency_quotations(date=None) -> None:
    pairs = (('USD', 'RUB'), ('EUR', 'RUB'), ('EUR', 'USD'))
    for main, second in pairs:
        df = yf.Ticker(f'{main}{second}=X').history().reset_index()
        if not date:
            data = df.iloc[-1].to_dict()
        else:
            data = df[df['Date'] == date].iloc[0].to_dict()
        try:
            CurrencyCourse.objects.update_or_create(
                currency1=Currency.objects.get(currency_ticker=main),
                currency2=Currency.objects.get(currency_ticker=second),
                date=data['Date'],
                defaults={
                    'open': data['Open'],
                    'high': data['High'],
                    'low': data['Low'],
                    'close': data['Close'],
                })
        except IndexError:
            continue


@shared_task
def update_current_quotations(date=None) -> None:
    """
    Получает список акций сервиса.
    Создает новую запись в БД с текущей ценой или обновляет её.
    """
    tickers = Stock.objects.values_list('ticker_yf', flat=True)
    ids = Stock.objects.values_list('id', flat=True)

    df = yf.download(tickers=' '.join(tickers), period='1d', interval='1d', group_by='ticker')
    for ticker_yf, _id in zip(tickers, ids):
        if not date:
            data = df[ticker_yf].reset_index().iloc[-1].to_dict()
        else:
            data = df[df['Date'] == date][ticker_yf].reset_index().iloc[0].to_dict()
        try:
            StockPrice.objects.update_or_create(
                ticker_id=_id,
                date=data['Date'],
                defaults={
                    'open': data['Open'],
                    'high': data['High'],
                    'low': data['Low'],
                    'close': data['Close'],
                    'volume': data['Volume'],
                })
        except IndexError:
            continue

from stock.models import Stock, StockPrice, Currency, CurrencyCourse

from datetime import datetime
import yfinance as yf
from celery import shared_task


@shared_task
def update_currency_quotations(date=datetime.today().strftime('%Y-%m-%d')) -> None:
    pairs = (('USD', 'RUB'), ('EUR', 'RUB'), ('EUR', 'USD'))
    for main, second in pairs:
        try:
            df = yf.Ticker(f'{main}{second}=X').history().reset_index()
            data = df[df['Date'] == date].iloc[0].to_dict()
            CurrencyCourse.objects.update_or_create(
                currency1=Currency.objects.get(currency_ticker=main),
                currency2=Currency.objects.get(currency_ticker=second),
                date=date,
                defaults={
                    'open': data['Open'],
                    'high': data['High'],
                    'low': data['Low'],
                    'close': data['Close'],
                })
        except IndexError:
            continue


@shared_task
def update_current_quotations() -> None:
    """
    Получает список акций сервиса.
    Создает новую запись в БД с текущей ценой или обновляет её.
    """
    tickers = Stock.objects.values_list('ticker_yf', flat=True)
    ids = Stock.objects.values_list('id', flat=True)

    df = yf.download(tickers=' '.join(tickers), period='1d', interval='1d', group_by='ticker')
    for ticker_yf, _id in zip(tickers, ids):
        data = df[ticker_yf].reset_index().iloc[-1].to_dict()
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

from stock.models import Stock, StockPrice

from datetime import datetime
import yfinance as yf
from celery import shared_task


@shared_task
def update_quotations(date= datetime.today().strftime('%Y-%m-%d')) -> None:
    """
    Получает список акций сервиса.
    Создает новую запись в БД с текущей ценой или обновляет её.
    """
    for ticker_yf, id in Stock.objects.values_list('ticker_yf', 'id'):
        try:
            df = yf.Ticker(ticker_yf).history().reset_index()
            data = df[df['Date'] == date].iloc[0].to_dict()
            StockPrice.objects.update_or_create(ticker_id=id,
                                                date=date,
                                                defaults={
                                                    'open': data['Open'],
                                                    'high': data['High'],
                                                    'low': data['Low'],
                                                    'close': data['Close'],
                                                    'volume': data['Volume']})
            print(f'{ticker_yf} updated')

        except:
            pass

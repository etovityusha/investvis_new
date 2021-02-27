import urllib
import requests
from lxml.html import fromstring
from bs4 import BeautifulSoup
from pandas_datareader import data as pdr
from datetime import datetime

from investvis.sqlalchemy_connect_db import create_alchemy_connect
from stock.models import Sector, Industry, Currency, Stock


def download_and_save_stock_data(obj):
    obj.ticker_yf = obj.ticker
    if obj.currency == Currency.objects.get(currency_ticker='RUB'):
        obj.ticker_yf += '.ME'
    sector, name, industry = _download_stock_info_from_yahoo_finance_website(obj.ticker_yf)
    try:
        obj.sector = Sector.objects.get(sector_title=sector)
    except Sector.DoesNotExist:
        obj.sector = Sector.objects.create(sector_title=sector, sector_rus=sector)
    try:
        obj.industry = Industry.objects.get(industry_title=industry, sector=obj.sector)
    except Industry.DoesNotExist:
        obj.industry = Industry.objects.create(industry_title=industry, industry_rus=industry, sector=obj.sector)
    obj.name = name
    try:
        _save_logo_from_tinkoff(obj.ticker)
        obj.logo = f'assets/images/logos/{obj.ticker}.png'
    except:
        pass
    return obj


def _download_stock_info_from_yahoo_finance_website(stock_ticker: str) -> tuple:
    page = requests.get(f'https://finance.yahoo.com/quote/{stock_ticker}/profile?p={stock_ticker}')
    tree = fromstring(page.content)
    sector = tree.xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/'
                        'div[1]/div/div/p[2]/span[2]/text()')[0]
    name = tree.xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/'
                      'div[1]/div/h3/text()')[0]
    industry = tree.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[4]/text()')[0]
    return sector, name, industry


def _save_logo_from_tinkoff(stock_ticker: str):
    page = requests.get(f'https://www.tinkoff.ru/invest/stocks/{stock_ticker}/')
    soup = BeautifulSoup(page.content)
    logo_img = soup.findAll('span', {'class': 'Avatar-module__image_2WFrC'})
    image_url = 'http://' + _find_between(str(logo_img[0]), 'background-image:url(//', ')"></span>')
    urllib.request.urlretrieve(image_url, f"assets/images/logos/{stock_ticker}.png")


def _find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def download_stock_quotations(yahoo_finance_tickers: list, table_name='stock_stockprice') -> None:
    """
    Скачивает с yahoo finance и сохраняет в базе данных котировки акции с 2015 года
    """
    engine = create_alchemy_connect()

    for ticker in yahoo_finance_tickers:
        try:
            df = pdr.get_data_yahoo(ticker, start="2015-01-01", end=datetime.now().strftime("%Y-%m-%d")).reset_index()
            df['ticker_id'] = str(Stock.objects.get(ticker=ticker.replace('.ME', '')).id)
            df = df.drop(['Adj Close'], 1).rename({'Date': 'date', 'Open': 'open', 'High': 'high',
                                                   'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, axis=1)
            df.to_sql(table_name, engine, if_exists='append', index=False)

        except Exception as ex:
            print(ticker, ex)

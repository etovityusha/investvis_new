import urllib
import requests
from lxml.html import fromstring
from bs4 import BeautifulSoup
from .. import models


def download_and_save_stock_data(obj):
    obj.ticker_yf = obj.ticker
    if obj.currency == models.Currency.objects.get(currency_ticker='RUB'):
        obj.ticker_yf += '.ME'
    sector, name, industry = _download_stock_info_from_yahoo_finance_website(obj.ticker_yf)
    obj.sector = models.Sector.objects.get(sector_title=sector)
    try:
        obj.industry = models.Industry.objects.get(industry_title=industry, sector=obj.sector)
    except:
        obj.industry = models.Industry.objects.create(industry_title=industry, sector=obj.sector)
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
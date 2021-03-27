from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers

from stock.models import Stock, StockPrice


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Stock List': '/stock-list/',
        'Stock Quotes': '/quotes/<str:ticker>/'
    }
    return Response(api_urls)


@api_view(['GET'])
def stock_list(request):
    stocks = Stock.objects.all()
    serializer = serializers.StockSerializer(stocks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def stock_quotes(request, ticker):
    stock = Stock.objects.get(ticker=ticker)
    prices = StockPrice.objects.filter(ticker=stock).order_by('date')
    serializer = serializers.StockPriceSerializer(prices, many=True)
    ret = []
    for el in serializer.data:
        ret.append([float(el['date']), float(el['close'])])
    return Response(ret)

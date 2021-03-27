from rest_framework import serializers
from stock.models import Stock, StockPrice


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['ticker', 'name']


class StockPriceSerializer(serializers.ModelSerializer):
    date = serializers.CharField(source='date_to_timestamp_in_ms')

    class Meta:
        model = StockPrice
        fields = ['date', 'close']

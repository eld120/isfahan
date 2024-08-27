from datetime import datetime, timedelta
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework.response import Response
from .models import Stock
from .models import StockImport
from .models import StockPrice


class StockSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="market:stock-detail",
        lookup_field="pk",
    )

    class Meta:
        model = Stock
        fields = ("name", "ticker")


class StockImportSerializer(serializers.ModelSerializer):
    stock = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="market:stock-detail",
         lookup_field="pk",
    )

    class Meta:
        model = StockImport
        fields = ("stock", "price", "date", "change", "change_percentage", "volume")


class StockPriceSerializer(serializers.ModelSerializer):
    stock = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="market:stock-detail",
         lookup_field="pk",
    )

    class Meta:
        model = StockPrice
        fields = ("stock", "price", "date", "volume")

    @action(detail=False, methods=['get'])
    def get_ticker_deets(self, request):
        ticker = request.query_params.get('ticker')
        days = int(request.query_params.get('days', 5))

        if not ticker:
            return Response(' ticker required')
        today = datetime.now()
        start = today - timedelta(days=days)
        stocks = StockPrice.objects.filter(ticker=ticker, date__range=[start, today])
        serializer = StockPriceSerializer(stocks, many=True)
        return Response(serializer.data)

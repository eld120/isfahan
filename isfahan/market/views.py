from decimal import Decimal
from decimal import getcontext

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
from isfahan.market.models import Stock
from isfahan.market.models import StockImport
from isfahan.market.models import StockPrice
from isfahan.market.serializers import StockImportSerializer
from isfahan.market.serializers import StockPriceSerializer
from isfahan.market.serializers import StockSerializer


class StockViewset(viewsets.ModelViewSet):
    model = Stock
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    def get_queryset(self):
        pk_list = self.request.query_params.get("pk")

        if pk_list:
            return Stock.objects.filter(id__in=[int(pk) for pk in pk_list.split(",")])
        return Stock.objects.all()


class StockImportViewset(viewsets.ModelViewSet):
    model = StockImport
    serializer_class = StockImportSerializer
    queryset = StockImport.objects.all()


class StockPriceViewset(viewsets.ModelViewSet):
    model = StockPrice
    serializer_class = StockPriceSerializer
    queryset = StockPrice.objects.all()

    @action(detail=False, methods=["get"])
    def get_market_trends(self, request):
        ticker = request.query_params.get("ticker", "")
        stock_name = request.query_params.get("name", "")
        queryset = (
            StockPrice.objects.select_related("stock", "previous")
            .filter(
                Q(stock__name__icontains=stock_name)
                | Q(stock__ticker__icontains=ticker),
            )
            .filter(date=StockPrice.objects.latest("date").date)
        )
        serializer = StockPriceSerializer(queryset, many=True)

        getcontext().prec = 4
        stock_prices = [
            {
                "company": record["stock"]["name"],
                "ticker": record["stock"]["ticker"],
                "date": record["date"],
                "price": Decimal(record["price"]),
                "percentage": 100
                * (Decimal(record["price"]) / Decimal(record["previous"]["price"]) - 1),
                "change": Decimal(record["price"])
                - Decimal(record["previous"]["price"]),
                "volume": int(record["volume"]),
            }
            for record in serializer.data
        ]

        return Response(stock_prices)

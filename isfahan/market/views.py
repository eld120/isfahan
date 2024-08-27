from rest_framework import viewsets

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


class StockImportViewset(viewsets.ModelViewSet):
    model = StockImport
    serializer_class = StockImportSerializer
    queryset = StockImport.objects.all()


class StockPriceViewset(viewsets.ModelViewSet):
    model = StockPrice
    serializer_class = StockPriceSerializer
    queryset = StockPrice.objects.all()

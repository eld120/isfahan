from rest_framework import viewsets

# Create your views here.
from .models import Stock
from .models import StockImport
from .serializers import StockImportSerializer
from .serializers import StockSerializer


class StockViewset(viewsets.ModelViewSet):
    model = Stock
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


class StockImportViewset(viewsets.ModelViewSet):
    model = StockImport
    serializer_class = StockImportSerializer
    queryset = StockImport.objects.all()
    lookup_field = "url"

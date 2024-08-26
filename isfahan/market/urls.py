from django.urls import include
from django.urls import path
from rest_framework import routers

from .views import StockImportViewset
from .views import StockPriceListView
from .views import StockViewset

router = routers.DefaultRouter()
router.register(r"stocks", StockViewset)
router.register(r"stock_markets", StockImportViewset)
router.register(r"stock_prices", StockPriceListView)


app_name = "market"

urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import include
from django.urls import path
from rest_framework import routers

from .views import StockImportViewset
from .views import StockPriceViewset
from .views import StockViewset

router = routers.DefaultRouter()
router.register(r"stocks", StockViewset, basename="stock")
router.register(r"stock_markets", StockImportViewset, basename="stock_market")
router.register(r"stock_prices", StockPriceViewset, basename="stock_price")


app_name = "market"

urlpatterns = [
    path("", include(router.urls)),
]

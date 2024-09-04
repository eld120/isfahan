from django.urls import include
from django.urls import path
from rest_framework import routers

from .views import StockImportViewset
from .views import StockPriceViewset
from .views import StockViewset

router = routers.DefaultRouter()
router.register(r"stocks", StockViewset, basename="stock")
router.register(r"stock-markets", StockImportViewset, basename="stock-market")
router.register(r"stock-prices", StockPriceViewset, basename="stock-price")


app_name = "market"

urlpatterns = [
    path("", include(router.urls)),
]

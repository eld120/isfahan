
from rest_framework import routers

from .views import StockViewset, StockImportViewset


router = routers.DefaultRouter()
router.register(r"stocks", StockViewset)
router.register(r"stock_markets", StockImportViewset)


app_name = "market"
urlpatterns = router.urls

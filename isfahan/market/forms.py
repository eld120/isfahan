from django.forms import ModelForm

from .models import Stock
from .models import StockImport
from .models import StockPrice


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ("name", "ticker")


class StockImportForm(ModelForm):
    class Meta:
        model = StockImport
        fields = ("stock", "price", "date", "change", "change_percentage", "volume")


class StockPriceForm(ModelForm):
    class Meta:
        model = StockPrice
        fields = ("stock", "price", "date", "volume")

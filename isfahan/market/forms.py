from django.forms import ModelForm
from .models import Stock, StockImport


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'ticker']

class StockImportForm(ModelForm):
    class Meta:
        model = StockImport
        fields = ['stock', 'price', 'date', 'change', 'change_percentage', 'volume']
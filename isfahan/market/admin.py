from django.contrib import admin

from .models import Stock
from .models import StockImport
from .models import StockPrice


# Register your models here.
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(StockImport)
class StockImportAdmin(admin.ModelAdmin):
    pass


@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    pass

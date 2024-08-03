from django.contrib import admin
from .models import Stock, StockImport
# Register your models here.
class StockAdmin(admin.ModelAdmin):
    pass

class StockImportAdmin(admin.ModelAdmin):
    pass


admin.site.register(Stock, StockAdmin)
admin.site.register(StockImport, StockImportAdmin)
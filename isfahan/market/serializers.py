from rest_framework import serializers

from .models import Stock
from .models import StockImport


class StockSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Stock
        fields = ('name', 'ticker')
        lookup_field = 'slug'
        extra_kwargs = {
            "url": {"view_name": "stock-detail", "lookup_field": "slug"},
        }


class StockImportSerializer(serializers.HyperlinkedModelSerializer):
    stock = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='stock-detail'
    )
    class Meta:
        model = StockImport
        fields = ('stock', 'price', 'date', 'change', 'change_percentage', 'volume')
        lookup_field = 'slug'
        extra_kwargs = {
            "url": {"view_name": "stockimport-detail", "lookup_field": "slug"},
        }

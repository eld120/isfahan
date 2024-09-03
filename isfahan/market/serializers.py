from rest_framework import serializers

from .models import Stock
from .models import StockImport
from .models import StockPrice


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("pk", "name", "ticker")


class StockImportSerializer(serializers.ModelSerializer):
    stock = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="market:stock-detail",
        lookup_field="pk",
    )

    class Meta:
        model = StockImport
        fields = ("stock", "price", "date", "change", "change_percentage", "volume")


class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = ("stock", "price", "previous", "date", "volume")
        depth = 1

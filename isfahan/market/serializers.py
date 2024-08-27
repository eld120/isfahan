from rest_framework import serializers

from .models import Stock
from .models import StockImport
from .models import StockPrice


class StockSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="stock-detail",
        lookup_field="url",
    )

    class Meta:
        model = Stock
        fields = ("name", "ticker")


class StockImportSerializer(serializers.ModelSerializer):
    stock = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="stock-detail",
    )

    class Meta:
        model = StockImport
        fields = ("stock", "price", "date", "change", "change_percentage", "volume")


class StockPriceSerializer(serializers.ModelSerializer):
    stock = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="stock-detail",
    )

    class Meta:
        model = StockPrice
        fields = ("stock", "price", "date", "volume")

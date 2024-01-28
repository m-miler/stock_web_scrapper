from scrapper.models.prices import StockPrices
from rest_framework import serializers


class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrices
        fields = "__all__"

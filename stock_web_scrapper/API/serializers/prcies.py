from scrapper.models.prices import StockPrices
from rest_framework import serializers


class PricesSerializer(serializers.ModelSerializer):
    close_daily_change = serializers.DecimalField(max_digits=15, decimal_places=2)
    class Meta:
        model = StockPrices
        fields = "__all__"

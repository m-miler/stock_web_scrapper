from scrapper.models.companies import StockCompanies
from rest_framework import serializers


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockCompanies
        fields = "__all__"

from django_filters import FilterSet, CharFilter
from scrapper.models.prices import StockPrices


class PricesFilters(FilterSet):
    class Meta:
        model = StockPrices
        fields = {"date": ['exact'],
                  'company_abbreviation': ['in', 'exact']}

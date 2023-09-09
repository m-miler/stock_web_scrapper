from django_filters import FilterSet, CharFilter
from scrapper.models.companies import StockCompanies


class CompaniesFilters(FilterSet):
    index = CharFilter(field_name='index', lookup_expr='icontains')

    class Meta:
        model = StockCompanies
        fields = ["index", 'company_abbreviation']

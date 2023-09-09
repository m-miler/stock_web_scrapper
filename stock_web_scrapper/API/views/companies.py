from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from scrapper.models.companies import StockCompanies
from ..serializers.companies import CompaniesSerializer
from ..filters.companies import CompaniesFilters


class Companies(ListModelMixin, GenericViewSet):
    queryset = StockCompanies.objects.all()
    serializer_class = CompaniesSerializer
    filterset_class = CompaniesFilters

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


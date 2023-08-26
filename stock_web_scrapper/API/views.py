from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from scrapper.models.companies import StockCompanies
from scrapper.models.prices import StockPrices
from .serializers.companies_serializer import CompaniesSerializer
from .serializers.prcies_serializer import PricesSerializer


class Companies(ListModelMixin, GenericViewSet):
    queryset = StockCompanies.objects.all()
    serializer_class = CompaniesSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class Prices (ListModelMixin, GenericViewSet):
    queryset = StockPrices.objects.all()
    serializer_class = PricesSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

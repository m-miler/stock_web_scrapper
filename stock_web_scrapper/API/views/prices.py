from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from scrapper.models.prices import StockPrices
from ..serializers.prcies import PricesSerializer
from ..filters.prices import PricesFilters


class Prices (ListModelMixin, GenericViewSet):
    queryset = StockPrices.objects.all()
    serializer_class = PricesSerializer
    filterset_class = PricesFilters

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

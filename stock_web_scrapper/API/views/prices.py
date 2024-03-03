from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from scrapper.models.prices import StockPrices
from ..serializers.prcies import PricesSerializer
from ..filters.prices import PricesFilters
from rest_framework.response import Response
from django.http.response import JsonResponse


class PricesList (ListModelMixin, GenericViewSet):
    queryset = StockPrices.objects.all()
    serializer_class = PricesSerializer
    filterset_class = PricesFilters

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_last_price(self, request):
        last_price = StockPrices.objects.filter(
            company_abbreviation=request.query_params.get('ticker')).latest('date')
        return JsonResponse({'last_price': last_price.close_price})
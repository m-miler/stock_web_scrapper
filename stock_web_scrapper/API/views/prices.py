from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from scrapper.models.prices import StockPrices
from ..serializers.prcies import PricesSerializer
from ..filters.prices import PricesFilters
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse


class PricesList (ListModelMixin, GenericViewSet):
    queryset = StockPrices.objects.all()
    serializer_class = PricesSerializer
    filterset_class = PricesFilters

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_last_price(self, request):
        try:
            last_price = StockPrices.objects.filter(
                company_abbreviation=request.query_params.get('ticker')).latest('date')
            serializer = self.get_serializer(last_price)
            return JsonResponse(serializer.data)

        except ObjectDoesNotExist:
            return JsonResponse({})

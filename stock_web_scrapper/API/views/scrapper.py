from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from scrapper.tasks import update_stock_prices, update_index_result
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

class Scrapper(ModelViewSet):

    def stock_update(self, request) -> Response:
        ticker = request.GET.getlist('s')
        start_date = request.GET.get('d1', None)
        end_date = request.GET.get('d2', None)
        interval = request.GET.get('i', None)
        response = update_stock_prices.apply_async(kwargs={'ticker':ticker,
                                                           'start_date':start_date,
                                                           'end_date':end_date, 'interval':interval
                                                           }, ignore_result=False)

        if response.get():
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_204_NO_CONTENT)

    def index_result_update(self, request) -> Response:
        ticker = request.GET.get('s')
        start_date = request.GET.get('d1', None)
        end_date = request.GET.get('d2', None)
        interval = request.GET.get('i', 'd')
        response = update_index_result.apply_async(kwargs={'ticker':ticker,
                                                           'start_date':start_date,
                                                           'end_date':end_date, 'interval':interval
                                                           }, ignore_result=False)
        if response.get():
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_204_NO_CONTENT)
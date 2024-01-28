from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from scrapper.tasks import update_stock_prices


class Scrapper(ModelViewSet):

    def stock_update(self, request) -> Response:
        ticker = request.GET.get('s')
        start_date = request.GET.get('d1', None)
        end_date = request.GET.get('d2', None)
        interval = request.GET.get('i', None)
        response = update_stock_prices(ticker=ticker, start_date=start_date, end_date=end_date, interval=interval)

        return response

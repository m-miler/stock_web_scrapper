from .views.companies import Companies
from .views.prices import PricesList
from .views.scrapper import Scrapper
from rest_framework.routers import DefaultRouter
from django.urls import re_path, path, include

router = DefaultRouter()
router.register(r"companies", Companies, basename="companies")
router.register(r"prices", PricesList, basename="prices")

urlpatterns = [
    path("", include(router.urls)),
    re_path(r'stocks/update/$',
            Scrapper.as_view({'get': 'stock_update'}), name='stock-update'),
    re_path(r'prices/last-price/$', PricesList.as_view({'get': 'get_last_price'}), name='stock-last-price')
]

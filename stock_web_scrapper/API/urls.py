from .views.companies import Companies
from .views.prices import PricesList
from .views.scrapper import Scrapper
from rest_framework.routers import DefaultRouter
from django.urls import re_path, path, include

router = DefaultRouter()
router.register(r"companies", Companies, basename="companies")
router.register(r"prices", PricesList, basename="prices-list")

urlpatterns = [
    path("", include(router.urls)),
    re_path(r'stock/update/$',
            Scrapper.as_view({'get': 'stock_update'}))
]

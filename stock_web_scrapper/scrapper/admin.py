from django.contrib import admin

from .models.companies import StockCompanies
from .models.prices import StockPrices

admin.site.register(StockCompanies)
admin.site.register(StockPrices)

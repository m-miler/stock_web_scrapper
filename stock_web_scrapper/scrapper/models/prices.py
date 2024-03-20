import datetime

from django.db import models

from ..models.companies import StockCompanies
from decimal import Decimal

from pandas.tseries.offsets import BDay

class StockPrices(models.Model):
    company_abbreviation = models.ForeignKey(
        StockCompanies,
        to_field="company_abbreviation",
        on_delete=models.CASCADE,
        help_text="Company Abbreviation",
    )
    date = models.DateField(help_text="Stock Price Date")
    open_price = models.DecimalField(
        help_text="Day Open Price", max_digits=15, decimal_places=2
    )
    max_price = models.DecimalField(
        help_text="Day Max Price", max_digits=15, decimal_places=2
    )
    min_price = models.DecimalField(
        help_text="Day Min Price", max_digits=15, decimal_places=2
    )
    close_price = models.DecimalField(
        help_text="Day Close Price", max_digits=15, decimal_places=2
    )
    volume = models.BigIntegerField(help_text="Day Volume")

    def __str__(self):
        return f"{self.company_abbreviation.company_abbreviation}_{self.date.strftime('%Y-%m-%d')}"

    def _calculate_daily_change(self, field_name):
        today = getattr(self, 'date')
        last_business_day = (today - BDay(1)).strftime("%Y-%m-%d")
        last_business_day_price = StockPrices.objects.filter(
            models.Q(date=last_business_day)
            & models.Q(
                company_abbreviation__company_abbreviation=self.company_abbreviation
            )
        ).first()
        if not last_business_day_price:
            return None

        current_value = getattr(self, field_name)
        last_day_price = getattr(last_business_day_price, field_name)
        daily_change = (current_value - last_day_price) / current_value
        return (Decimal(daily_change) * 100).quantize(Decimal("0.01"))

    def __getattr__(self, item):
        if "_daily_change" in item:
            field_name = f"{item.split('_')[0]}_price"
            return self._calculate_daily_change(field_name=field_name)
        else:
            return self.item

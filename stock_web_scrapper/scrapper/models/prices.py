from django.db import models

from ..models.companies import StockCompanies


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

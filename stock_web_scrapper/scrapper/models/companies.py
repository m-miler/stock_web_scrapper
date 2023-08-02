from django.db import models


class StockCompanies(models.Model):
    company_full_name = models.CharField(
        max_length=50, help_text="Full Name of the Company"
    )
    company_abbreviation = models.CharField(
        max_length=10, help_text="Company Abbreviation", unique=True
    )
    index = models.CharField(
        max_length=20, help_text="Company Stock Exchange Market Index"
    )

    def __str__(self):
        return self.company_abbreviation

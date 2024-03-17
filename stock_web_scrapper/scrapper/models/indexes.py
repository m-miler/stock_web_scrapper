from django.db import models


class Indexes(models.Model):
    ticker = models.CharField(max_length=10, unique=True, help_text="Index ticker")

class IndexResult(models.Model):
    index = models.ForeignKey(
        Indexes,
        related_name='index_result',
        to_field="ticker",
        on_delete=models.CASCADE,
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
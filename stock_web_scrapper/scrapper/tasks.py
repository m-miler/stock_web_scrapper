from celery import shared_task
from .models.companies import StockCompanies
from .scrappers.companies import CompaniesScrapper
from .scrappers.prices import PriceScrapper


@shared_task
def update_stock_prices() -> None:
    """
    Celery task to web scrapping stock prices for each company in a stock database.
    Task starts automatically at 24 o'clock and get data form the previous day.
    """

    companies = StockCompanies.objects.values_list("company_abbreviation", flat=True)

    for abbreviation in companies:
        PriceScrapper(ticker=abbreviation).save()


@shared_task
def update_companies() -> None:
    """
    Function to update the companies in database.
    :return: None
    """
    CompaniesScrapper().update()

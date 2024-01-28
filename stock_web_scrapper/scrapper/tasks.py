import click
from celery import shared_task
from rest_framework.response import Response
from .scrappers.companies import CompaniesScrapper
from .scrappers.prices import PriceScrapper


@shared_task
def update_stock_prices(ticker: str,
                        start_date: str,
                        end_date: str,
                        interval: str) -> Response:
    """
    Celery task to web scrapping stock prices for each company in a stock database.
    """
    return PriceScrapper(ticker=ticker, start=start_date, end=end_date, interval=interval).save_stock_price()


@shared_task
def update_companies() -> None:
    """
    Function to update the companies in database.
    :return: None
    """
    CompaniesScrapper().update()

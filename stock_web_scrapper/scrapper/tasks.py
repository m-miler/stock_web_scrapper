import click
from celery import shared_task
from rest_framework.response import Response
from .scrappers.companies import CompaniesScrapper
from .scrappers.prices import PriceScrapper
from .scrappers.index_result import IndexResultScrapper

@shared_task
def update_stock_prices(ticker: str | list,
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


@shared_task
def update_index_result(ticker: str | list,
                        start_date: str,
                        end_date: str,
                        interval: str) -> Response:
    """
    Celery task to web scrapping stock prices for each company in a stock database.
    """
    return IndexResultScrapper(ticker=ticker, start=start_date, end=end_date, interval=interval).save_stock_price()
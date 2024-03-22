from datetime import timedelta
from datetime import datetime
from celery import shared_task

from .scrappers.companies import CompaniesScrapper
from .scrappers.prices import PriceScrapper
from .scrappers.index_result import IndexResultScrapper
from .scrappers.indexes import GPWIndexes

from .models.companies import StockCompanies

@shared_task
def update_stock_prices(ticker: str | list,
                        start_date: str = None,
                        end_date: str = None,
                        interval: str = "d") -> bool:
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
def update_indexes() -> None:
    GPWIndexes().scrap_indexes()

@shared_task
def update_index_result(ticker: str | list,
                        start_date: str,
                        end_date: str,
                        interval: str) -> bool:
    """
    Celery task to web scrapping stock prices for each company in a stock database.
    """
    return IndexResultScrapper(ticker=ticker, start=start_date, end=end_date, interval=interval).save_stock_price()


@shared_task
def update_wig20():
    ticker_list = list(StockCompanies.objects.filter(index__contains='WIG20').values_list('company_abbreviation',
                                                                                          flat=True))
    pause = 3
    return PriceScrapper(ticker=ticker_list, pause=pause).save_stock_price()
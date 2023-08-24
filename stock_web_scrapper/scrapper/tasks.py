import datetime

from celery import shared_task
from .scrapper import Scrapper
from .models.companies import StockCompanies


@shared_task
def update_stock_prices(*args: tuple[any, ...], **kwargs: any) -> None:
    """
    Celery task to web scrapping stock prices for each company in a stock database.
    Task starts automatically at 24 o'clock and get data form the previous day.
    """

    companies = StockCompanies.objects.values_list("company_abbreviation", flat=True)
    start_day = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")

    for abbreviation in companies:
        company: str = abbreviation.get("company_abbreviation")
        Scrapper().save_price_data(company, start_day)


def update_companies() -> None:
    """
    Function to update the companies in database.
    :return:None
    """
    scrapper: Scrapper = Scrapper()
    companies: list[tuple[str, str, str]] = scrapper.companies_html_parser()

    for company in companies:
        scrapper.save_or_update_companies_data(company)


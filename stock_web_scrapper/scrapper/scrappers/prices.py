import datetime
import requests
import time

from ..models.companies import StockCompanies
from ..models.prices import StockPrices
from ..utils import sanitize_dates


class PriceScrapper:
    def __init__(
            self,
            ticker: str,
            start=None,
            end=None,
            pause=1,
            request_limit=None
    ):
        self.ticker = ticker
        start, end = sanitize_dates(start, end)
        self.start = start
        self.end = end
        self.pause = pause
        self.url = f"https://stooq.pl/q/d/l/?s={self.ticker}&d1={self.start}&d2={self.end}&i=d"
        self.request_counter = 0
        self.request_limit = request_limit

    def save(self) -> None:
        """
        Method to save web scrapped data to the database.
        :return: None
        """

        data = self._get_stock_data()
        time.sleep(self.pause)

        if data:
            date, open_price, max_price, min_price, close_price, volume = data
            company: StockCompanies = StockCompanies.objects.get(company_abbreviation=self.ticker)
            obj, created = StockPrices.objects.update_or_create(
                company_abbreviation=company,
                date=date,
                open_price=open_price,
                max_price=max_price,
                min_price=min_price,
                close_price=close_price,
                volume=volume
            )

    def _get_response(self) -> requests.Response or list:
        """
        Method to get response from website.
        :return: requests.Response or list
        """
        response = requests.get(url=self.url, timeout=3)
        if response.status_code == requests.codes.OK and response.text != 'Brak danych':
            self._requests_counter()
            return response
        else:
            self._error_logger(response.status_code, response.text)
            return []

    def _get_stock_data(self) -> list[str]:
        """
        Method with web scrapping code to get the stock price data.
        :return: list[str]
        """
        response = self._get_response()
        if response:
            stock_data = self._response_parser(response)
            return stock_data

        return response

    @staticmethod
    def _response_parser(data: requests.Response) -> list[str]:
        """
        Method to parse the response content to list of strings.
        :return: list[str]
        """
        return data.content.decode("utf-8").strip().split("\r\n")[1].split(",")

    def _requests_counter(self) -> None:
        """
        Method to count number of requestes.
        :return: None
        """
        self.request_counter += 1
        if self.request_counter == self.request_limit:
            self._sleep_until_midnight()

    @staticmethod
    def _sleep_until_midnight() -> None:
        """
        Staticmethod to sleep script until next day midnight in case of website request limitation policy.
        :return: None
        """
        today = datetime.datetime.today()
        next_day = datetime.datetime(today.year, today.month, today.day, 0, 0) + datetime.timedelta(days=1)
        time.sleep((next_day - today).total_seconds())

import datetime
import requests
import time
import logging
from ..models.companies import StockCompanies
from ..models.prices import StockPrices
from ..utils import sanitize_dates

class PriceScrapper:
    def __init__(
            self,
            ticker: str | list,
            start=None,
            end=None,
            interval: str = "d",
            pause: int = 1,
            request_limit=None
    ):
        self.ticker = ticker if isinstance(ticker, list) else [ticker]
        start, end = sanitize_dates(start, end)
        self.start = start
        self.end = end
        self.interval = interval
        self.pause = pause
        self.request_counter = 0
        self.request_limit = request_limit

    def _set_url(self, ticker: str) -> str:
        return f"https://stooq.pl/q/{self.interval}/l/?s={ticker}&d1={self.start}&d2={self.end}&i={self.interval}"

    def save_stock_price(self) -> bool:
        """
        Method to save web scrapped data to the database.
        :return: None
        """
        for i, ticker in enumerate(self.ticker):
            data: list[str] = self._get_stock_data(self._set_url(ticker=ticker))
            time.sleep(self.pause)

            if len(data) > 0:
                for item in data[1:]:
                    self._save_to_db(item, ticker)

            if i == len(self.ticker)-1: return True
        return False

    def _save_to_db(self, data: str, ticker: str):
        if data:
            try:
                date, open_price, max_price, min_price, close_price, volume = data.split(',')
                company: StockCompanies = StockCompanies.objects.get(company_abbreviation=ticker)
                obj, created = StockPrices.objects.update_or_create(
                    company_abbreviation=company,
                    date=date,
                    defaults={
                    'open_price':open_price,
                    'max_price':max_price,
                    'min_price':min_price,
                    'close_price':close_price,
                    'volume':volume}
                )

            except Exception as error:
                logging.error(error)

    def _get_response(self, url: str) -> requests.Response or list:
        """
        Method to get response from website.
        :return: requests.Response or list
        """
        response = requests.get(url=url, timeout=3)
        if response.status_code == requests.codes.OK and response.text != 'Brak danych':
            self._requests_counter()
            return response
        else:
            logging.debug(response.text)
            return []

    def _get_stock_data(self, url: str) -> list[str]:
        """
        Method with web scrapping code to get the stock price data.
        :return: list[str]
        """
        response = self._get_response(url=url)
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
        return data.content.decode("utf-8").strip().splitlines()

    def _requests_counter(self) -> None:
        """
        Method to count number of requests.
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

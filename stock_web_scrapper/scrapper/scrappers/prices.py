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
            pause=1
    ):
        self.ticker = ticker
        start, end = sanitize_dates(start, end)
        self.start = start
        self.end = end
        self.pause = pause
        self.url = f"https://stooq.pl/q/d/l/?s={self.ticker}&d1={self.start}&d2={self.end}&i=d"

    def save(self) -> None:
        """
        Function to save web scrapped data to the stock_price database.
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

        response = requests.get(url=self.url, timeout=3)
        if response.status_code == requests.codes.OK and response.text != 'Brak danych':
            return response
        else:
            self._error_logger(response.status_code, response.text)
            return []

    def _get_stock_data(self) -> list[str]:
        """
        Function with web scrapping code to get the stock price data.
        :return: list[str]
        """
        response = self._get_response()
        if response:
            stock_data = self._response_parser(response)
            return stock_data

        return response

    def _error_logger(self, status_code, text) -> None:
        with open(f'scrapper/logs/error_log_{self.start}.txt', 'a') as file:
            file.write(f'Ticker: {self.ticker}; Date: {self.start}; StatusCode: {status_code}; Reason: {text}')
            file.write('\n')

    @staticmethod
    def _response_parser(data: requests.Response) -> list[str]:
        return data.content.decode("utf-8").strip().split("\r\n")[1].split(",")

# import datetime

import requests

from bs4 import BeautifulSoup
from .models.companies import StockCompanies
from .models.prices import StockPrices


class Scrapper:

    def get_companies_data(self) -> list[str]:
        url = "https://www.gpw.pl/spolki"
        request = requests.get(url)
        companies_table = BeautifulSoup(request.text, "html.parser").\
            find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == 'lista-spolek')
        companies = companies_table.findAll(lambda tag: tag.name == 'tr')

        for company in companies:
            company_name = company.find_all('a')
            company_name = company.find(attrs={'class': 'name'}).find(text=True).strip()
            ticker = company.find(attrs={'class': 'name'}).find('span').text.strip()
        return companies

    def get_stock_data(self, company: str, start_day) -> list[str]:
        """
        Function with web scrapping code to get the stock price data.
        :param company: Company abbreviation passed from celery task
        :param start_day: Date from which we want to get data
        :return: list[str]
        """
        url = f"https://stooq.pl/q/d/l/?s={company}&d1={start_day}&d2={start_day}&i=d"
        response = requests.get(url=url).content.decode("utf-8").strip().split("\r\n")
        stock_data = response[1].split(",")
        return stock_data

    def save_data(self, company: str, start_day) -> None:
        """
        Function to save web scrapped data to the stock_price database.
        :param company: company abbreviation passed from celery task
        :param start_day: date from which we want to get data
        :return: None
        """

        date, open_price, max_price, min_price, close_price, volume = self.get_stock_data(company, start_day)
        company = StockCompanies.objects.get(company_abbreviation=company)

        entity = StockPrices(
            company_abbreviation=company,
            date=date,
            open_price=open_price,
            max_price=max_price,
            min_price=min_price,
            close_price=close_price,
            volume=volume
        )
        entity.save()

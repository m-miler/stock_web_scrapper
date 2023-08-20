# import datetime
import bs4
import requests
import time

from bs4 import BeautifulSoup
from .models.companies import StockCompanies
from .models.prices import StockPrices
from selenium import webdriver
from selenium.webdriver.common.by import By


class Scrapper:

    def companies_html_parser(self) -> list[tuple[str, str, str]]:
        """
        Function with web scrapping code to get the companies information data.
        :return: list[tuple[str, str, str]]
        """
        companies_list: list = []
        data = self._get_companies_table()
        companies = data.findAll(lambda tag: tag.name == 'tr')

        for company in companies[1:]:
            company_name: str = company.find(attrs={'class': 'name'}).find(text=True).strip()
            ticker: str = company.find(attrs={'class': 'name'}).find('span').text.strip()[1:4]
            index: str = self._split_index(company.text)
            company_info: tuple[str, str, str] = (company_name, ticker, index)
            companies_list.append(company_info)

        return companies_list

    def _get_companies_table(self) -> bs4.Tag:
        """
        Method to get full companies list from GPW website.
        :return: bs4.Tag
        """
        url: str = "https://www.gpw.pl/spolki"
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(3)

        companies_number = int(driver.find_element(By.ID, 'count-all').text)
        data_limit = int(driver.find_element(By.CLASS_NAME, 'more').get_attribute('data-limit'))
        click_limit = int(round((companies_number - data_limit) / data_limit, 0))

        for i in range(1, click_limit):
            show_more = driver.find_element(By.XPATH, "//*[contains(text(), 'Pokaż więcej ')]")
            driver.execute_script("arguments[0].click();", show_more)
            time.sleep(3)

        request = driver.page_source
        companies_table = BeautifulSoup(request, "html.parser").\
            find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == 'lista-spolek')

        return companies_table

    def _split_index(self, text: str) -> str:
        return ";".join([x.strip() for x in text.split('\n\n\n')[2].split("|")[1].split(",")])

    def save_or_update_companies_data(self, company_data: tuple) -> None:
        """
        Function to save web scrapped data to the companies table in database.
        :param company_data: companies info data
        :return: None
        """
        entity: StockCompanies = StockCompanies(
            company_full_name=company_data[0],
            company_abbreviation=company_data[1],
            index=company_data[2]
        )
        entity.save()

    def _get_stock_data(self, company: str, start_day) -> list[str]:
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

    def save_price_data(self, company: str, start_day: str) -> None:
        """
        Function to save web scrapped data to the stock_price database.
        :param company: company abbreviation passed from celery task
        :param start_day: date from which we want to get data
        :return: None
        """

        date, open_price, max_price, min_price, close_price, volume = self._get_stock_data(company, start_day)
        company: StockCompanies = StockCompanies.objects.get(company_abbreviation=company)

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

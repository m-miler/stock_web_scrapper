import bs4
import time

from bs4 import BeautifulSoup
from ..models.companies import StockCompanies
from selenium import webdriver
from selenium.webdriver.common.by import By


class CompaniesScrapper:

    def __init__(self):
        self.url: str = "https://www.gpw.pl/spolki"
        self.show_more_txt: str = "//*[contains(text(), 'Pokaż więcej ')]"
        self.driver: webdriver.Chrome = webdriver.Chrome()
        self.driver.get(self.url)
        self.companies_list: list = []

    def update(self):
        self._get_companies()
        for company in self.companies_list:
            self.save(company)

    @staticmethod
    def save(company_data: tuple) -> None:
        """
        Function to save web scrapped data to the companies table in database.
        :param company_data: companies info data
        :return: None
        """
        obj, created = StockCompanies.objects.update_or_create(
            company_full_name=company_data[0],
            company_abbreviation=company_data[1],
            index=company_data[2]
        )

    def _get_companies(self) -> None:
        """
        Function with web scrapping code to get the companies information data.
        :return: list[tuple[str, str, str]]
        """
        data = self._get_companies_table()
        companies = data.findAll(lambda tag: tag.name == 'tr')

        for company in companies[1:]:
            company_name: str = company.find(attrs={'class': 'name'}).find(text=True).strip()
            ticker: str = company.find(attrs={'class': 'name'}).find('span').text.strip()[1:4]
            index: str = self._split_index(company.text)
            company_info: tuple[str, str, str] = (company_name, ticker, index)
            self.companies_list.append(company_info)

    def _get_companies_table(self) -> bs4.Tag:
        """
        Method to get full companies list from GPW website.
        :return: bs4.Tag
        """

        click_limit = self._calculate_click_limit()

        for i in range(1, click_limit):
            show_more = self.driver.find_element(By.XPATH, self.show_more_txt)
            self.driver.execute_script("arguments[0].click();", show_more)
            time.sleep(3)

        request = self.driver.page_source
        companies_table = BeautifulSoup(request, "html.parser").\
            find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == 'lista-spolek')

        return companies_table

    @staticmethod
    def _split_index(text: str) -> str:
        return ";".join([x.strip() for x in text.split('\n\n\n')[2].split("|")[1].split(",")])

    def _calculate_click_limit(self):
        companies_number = int(self.driver.find_element(By.ID, 'count-all').text)
        data_limit = int(self.driver.find_element(By.CLASS_NAME, 'more').get_attribute('data-limit'))
        return int(round((companies_number - data_limit) / data_limit, 0))

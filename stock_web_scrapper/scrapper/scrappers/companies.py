import bs4
import time

from bs4 import BeautifulSoup
from ..models.companies import StockCompanies
from selenium import webdriver
from selenium.webdriver.common.by import By


class CompaniesScrapper:

    def __init__(self):
        self.url: str = "https://www.gpw.pl/list-of-companies"
        self.show_more_txt: str = "//*[contains(text(), 'Show more ')]"

    def _prepare_webdriver(self) -> webdriver:
        options: webdriver.ChromeOptions = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        options.add_argument('--disable-dev-shm-using')
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--no-sandbox")
        driver: webdriver = webdriver.Chrome(options=options)
        driver.get(self.url)

        try:
            cookies = driver.find_element(By.ID, "onetrust-accept-btn-handler")
            driver.execute_script("arguments[0].click();", cookies)
        except:
            pass

        return driver
    def update(self):
        companies_list: list[dict] = self._get_companies()
        for company in companies_list:
            self._save(company)

    @staticmethod
    def _save(company_info: dict[str]) -> None:
        """
        Function to save web scrapped data to the companies table in database.
        :param company_info: companies info data
        :return: None
        """
        obj, created = StockCompanies.objects.update_or_create(
            company_full_name=company_info['company_name'],
            company_abbreviation=company_info['ticker'],
            index=company_info['index']
        )

    def _get_companies(self) -> list[dict]:
        """
        Function with web scrapping code to get the companies information data.
        :return: list[tuple[str, str, str]]
        """
        companies_list: list[dict] = []
        data = self._get_companies_table()
        companies = data.findAll(lambda tag: tag.name == 'tr')

        for company in companies[1:]:
            company_info: dict[str, str, str] = {
                'company_name': company.find(attrs={'class': 'name'}).find(text=True).strip(),
                'ticker': company.find(attrs={'class': 'name'}).find('span').text.strip()[1:4],
                'index': self._split_index(company.text)}
            companies_list.append(company_info)

        return companies_list

    def _get_companies_table(self) -> bs4.Tag:
        """
        Method to get full companies list from the website.
        :return: bs4.Tag
        """
        driver: webdriver = self._prepare_webdriver()
        click_limit = self._calculate_click_limit(driver)

        for i in range(1, click_limit):
            show_more = driver.find_element(By.XPATH, self.show_more_txt)
            driver.execute_script("arguments[0].click();", show_more)
            time.sleep(3)

        request = driver.page_source
        companies_table = BeautifulSoup(request, "html.parser").\
            find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == 'lista-spolek')

        return companies_table

    def _split_index(self, text: str) -> str:
        return ";".join([x.strip() for x in text.split('\n\n\n')[2].split("|")[1].split(",")])

    def _calculate_click_limit(self, driver: webdriver):
        companies_number = int(driver.find_element(By.ID, 'count-all').text)
        data_limit = int(driver.find_element(By.CLASS_NAME, 'more').get_attribute('data-limit'))
        return int(round((companies_number - data_limit) / data_limit, 0))

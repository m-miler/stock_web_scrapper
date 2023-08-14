import bs4
from django.test import TestCase
from datetime import datetime
from unittest.mock import patch
from ..scrapper import Scrapper
from ..models.prices import StockPrices
from ..models.companies import StockCompanies


class ScrapperTest(TestCase):
    def setUp(self) -> None:
        self.date = "20230801"
        self.company = StockCompanies.objects.create(company_full_name="CD Project", company_abbreviation="CDR", index="WIG20")
        self.scrapper = Scrapper()

    def test_if_get_stock_data_make_a_correct_request(self):
        data = self.scrapper.get_stock_data(self.company.company_abbreviation, self.date)
        self.assertIsInstance(data, list)

    @patch.object(Scrapper, 'get_stock_data', return_value=["2023-08-01", "10.0", "15.0", "5.0", "12.5", "100"])
    def test_if_a_new_entity_is_created_in_db(self, get_stock_data):

        self.scrapper.save_price_data(self.company.company_abbreviation, self.date)
        stock_price = StockPrices.objects.get(
            company_abbreviation=self.company, date=datetime.strptime(self.date, "%Y%m%d").strftime("%Y-%m-%d")
        )
        self.assertEqual(
            stock_price.company_abbreviation.company_full_name,
            self.company.company_full_name,
        )
        self.assertIsInstance(stock_price.company_abbreviation, StockCompanies)
        self.assertEqual(stock_price.open_price, 10.0)

    def test_if_get_companies_table_create_a_correct_request(self):
        data = self.scrapper.get_companies_table()
        self.assertIsInstance(data, bs4.Tag)

    def test_companies_html_parser(self):
        data = self.scrapper.companies_html_parser()
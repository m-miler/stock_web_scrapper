import os
import requests

from decimal import Decimal
from django.test import TestCase
from datetime import datetime
from unittest.mock import patch
from ..models.prices import StockPrices
from ..models.companies import StockCompanies
from ..scrappers.prices import PriceScrapper


class PriceScrapperTest(TestCase):
    def setUp(self) -> None:
        self.date = "20230801"
        self.company = StockCompanies.objects.create(
            company_full_name="CD Project", company_abbreviation="CDR", index="WIG20")
        self.price_scrapper = PriceScrapper(self.company.company_abbreviation, self.date)
        self.url = f"https://stooq.pl/q/d/l/?s={self.company.company_abbreviation}&d1={self.date}&d2={self.date}&i=d"

    def tearDown(self) -> None:
        try:
            os.remove(f'scrapper/logs/error_log_{self.date}.txt')
        except OSError:
            pass

    @staticmethod
    def file_exists(path):
        return os.path.exists(path)

    def test_if_get_response_make_a_correct_request(self):
        response = self.price_scrapper._get_response()
        self.assertNotEquals(response, [])
        self.assertEqual(response.status_code, requests.codes.OK)

    def test_if_get_response_log_errors(self):
        scrapper = PriceScrapper(ticker='XXX', start=self.date)
        response = scrapper._get_response()
        self.assertEqual(response, [])
        self.assertTrue(self.file_exists(f'scrapper/logs/error_log_{self.date}.txt'))

    @patch.object(PriceScrapper,
                  '_get_response',
                  return_value=[]
                  )
    def test_if_get_stock_data_return_empty_list(self, _get_response):
        data = self.price_scrapper._get_stock_data()
        self.assertEqual(data, [])

    def test_if_a_new_price_entry_is_created_in_db(self):

        self.price_scrapper.save()
        stock_price = StockPrices.objects.get(
            company_abbreviation=self.company, date=datetime.strptime(self.date, "%Y%m%d").strftime("%Y-%m-%d")
        )
        self.assertEqual(
            stock_price.company_abbreviation.company_full_name,
            self.company.company_full_name,
        )
        self.assertIsInstance(stock_price.company_abbreviation, StockCompanies)
        self.assertEqual(stock_price.open_price, Decimal('162.50'))
        self.assertEqual(stock_price.max_price, Decimal('162.50'))
        self.assertEqual(stock_price.close_price, Decimal('160.80'))
        self.assertEqual(stock_price.volume, Decimal('202070.0'))



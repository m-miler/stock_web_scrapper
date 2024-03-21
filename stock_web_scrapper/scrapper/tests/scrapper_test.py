import pytest

from django.urls import reverse
from unittest import mock

from ..scrappers.companies import CompaniesScrapper
from ..models.companies import StockCompanies
@pytest.fixture
def mocked_get_companies(test_company_price):
    with mock.patch.object(CompaniesScrapper, "_get_companies",
                    return_value=[{'company_name': test_company_price.company_abbreviation.company_full_name,
                                    'ticker': test_company_price.company_abbreviation.company_abbreviation,
                                    'index': test_company_price.company_abbreviation.index}]):
        result = CompaniesScrapper()
        yield result

@pytest.mark.django_db
def test_if_companies_scrapper_add_new_record_to_db(mocked_get_companies, django_db_setup, test_company_price):
    CompaniesScrapper().update()
    company = StockCompanies.objects.get(
        company_abbreviation=test_company_price.company_abbreviation.company_abbreviation)
    assert company.company_abbreviation == test_company_price.company_abbreviation.company_abbreviation
    assert isinstance(company, StockCompanies)
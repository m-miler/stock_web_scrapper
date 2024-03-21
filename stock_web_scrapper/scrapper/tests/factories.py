import string

import factory

from ..models.companies import StockCompanies
from ..models.prices import StockPrices


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockCompanies
        django_get_or_create = ("company_abbreviation",)

    company_full_name = factory.Faker("pystr", min_chars=3, max_chars=10)
    company_abbreviation = factory.Faker(
        "pystr_format", string_format="???", letters=string.ascii_uppercase
    )
    index = "WIG20"


class StockPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockPrices

    company_abbreviation = factory.SubFactory(CompanyFactory)
    date = factory.Sequence(lambda n: f"2023-01-{n+1:02}")
    open_price = factory.Faker(
        "pyfloat", min_value=133.00, max_value=134.00, right_digits=2
    )
    max_price = factory.Faker(
        "pyfloat", min_value=133.00, max_value=134.00, right_digits=2
    )
    min_price = factory.Faker(
        "pyfloat", min_value=133.00, max_value=134.00, right_digits=2
    )
    close_price = factory.Faker(
        "pyfloat", min_value=133.00, max_value=134.00, right_digits=2
    )
    volume = factory.Faker("pyint", min_value=25000, max_value=1000000)

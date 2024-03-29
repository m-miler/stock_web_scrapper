import pytest
from django.db import connections
from django.core.management import call_command

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .factories import CompanyFactory, StockPriceFactory

def run_sql(sql):
    conn = psycopg2.connect(database='postgres', user='postgres', password='postgres', host='localhost')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    from django.conf import settings

    settings.DATABASES['default']['NAME'] = 'stocks'
    settings.DATABASES['default']['USER'] = 'postgres'
    settings.DATABASES['default']['PASSWORD'] = 'postgres'
    settings.DATABASES['default']['HOST'] = 'localhost'

    run_sql('DROP DATABASE IF EXISTS stocks')
    run_sql('CREATE DATABASE stocks')
    with django_db_blocker.unblock():
        call_command('migrate', '--noinput')
    yield

    for connection in connections.all():
        connection.close()

    run_sql('DROP DATABASE stocks')


@pytest.fixture
def test_company():
    return CompanyFactory()

@pytest.fixture
def test_company_price(test_company):
    return StockPriceFactory(company_abbreviation=test_company)
from django.core.management.base import BaseCommand, CommandError
from scrapper.scrappers.companies import CompaniesScrapper


class Command(BaseCommand):
    help = 'Populate database with stock companies name from GPW site.'

    def handle(self, *args, **options):
        CompaniesScrapper().update()
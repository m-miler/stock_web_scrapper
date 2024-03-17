from django.core.management.base import BaseCommand, CommandError
from scrapper.scrappers.indexes import GPWIndexes


class Command(BaseCommand):
    help = 'Populate database with stock companies name from GPW site.'

    def handle(self, *args, **options):
        GPWIndexes().scrap_indexes()
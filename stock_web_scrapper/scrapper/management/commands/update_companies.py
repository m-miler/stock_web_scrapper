from django.core.management.base import BaseCommand, CommandError
from scrapper.tasks import update_companies


class Command(BaseCommand):
    help = 'Populate database with stock companies name from GPW site.'

    def handle(self, *args, **options):
        update_companies()
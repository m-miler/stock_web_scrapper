import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_web_scrapper.settings')

app = Celery('stock_web_scrapper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

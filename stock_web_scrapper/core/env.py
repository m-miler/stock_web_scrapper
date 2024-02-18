import environ
from django.core.management.utils import get_random_secret_key

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, get_random_secret_key()),
    # POSTGRES
    POSTGRES=(bool, True),
    DB_NAME=(str, "stocks"),
    DB_USER=(str, "postgres"),
    DB_PASSWORD=(str, "postgres"),
    DB_HOST=(str, "db"),
    DB_PORT=(str, "5432"),
    # Celery
    CELERY_BROKER=(str, "redis://redis:6379/0"),
    ALLOWED_HOSTS=(list, []),
)

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbitrage.settings")

app = Celery("arbitrage")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secrets_detection.settings')

app = Celery('secrets_detection')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# BankingSystem/celery.py
import os
from celery import Celery
from django.conf import settings
from datetime import datetime, timedelta

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BankingSystem.settings')

app = Celery('BankingSystem')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Periodic task configuration
app.conf.beat_schedule = {
    'calculate-hourly-interest': {
        'task': 'accounts.tasks.calculate_hourly_interest',
        'schedule': timedelta(hours=1),  # Run hourly
    },
    'generate-daily-interest-report': {
        'task': 'accounts.tasks.calculate_daily_interest_summary',
        'schedule': timedelta(days=1),  # Run daily
    },
    'check-dormant-accounts': {
        'task': 'accounts.tasks.deactivate_dormant_accounts',
        'schedule': timedelta(days=90),  # Run quarterly
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
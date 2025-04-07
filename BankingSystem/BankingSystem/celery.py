import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BankingSystem.settings')

app = Celery('BankingSystem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Using the database-backed scheduler
app.conf.beat_schedule = {
    'calculate-every-30-seconds': {
        'task': 'accounts.tasks.calculate_30s_interest',
        'schedule': 30.0,  # Run every 30 seconds
        'options': {
            'expires': 15.0,  # Expire after 15 seconds if not run
            'retry': True,  # Enable retries
            'retry_policy': {
                'max_retries': 3,
                'interval_start': 10,
                'interval_step': 10,
                'interval_max': 30,
            }
        }
    },
}
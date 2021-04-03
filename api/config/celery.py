import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_url = BASE_REDIS_URL
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'




app.conf.beat_schedule = {
    'sync_script': {
        'task': 'sync_plants',
        'schedule': 84600.0,
        # 'schedule': 60.0,
        'args': ()
    },
    'integration_script': {
        'task': 'integration',
        # 'schedule': 45.0,
        'schedule': 3000.0,
        'args': ()
    },
}

import os
import logging
from django.conf import settings
from celery import Celery
from celery.schedules import crontab


logger = logging.getLogger("Celery")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MGC.settings')
app = Celery('MGC')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    

app.conf.beat_schedule = {
    #Scheduler Name

}
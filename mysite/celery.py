import os
from celery import Celery
from celery.beat import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
app = Celery('mysite')

# app.conf.beat_schedule = {
#     'check_slot_time_crontab' : {
#         'task' : 'CheckSlotTime',
#         'schedule' : 60.0,
#     },
# }

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


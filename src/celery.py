# В первую очередь мы импортируем библиотеку для работы с операционной системой и саму библиотеку Celery.
import os
from celery import Celery
from celery.schedules import crontab

from src import settings

# Второй строчкой мы связываем настройки Django с настройками Celery через переменную окружения.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

app = Celery('GoodNews')
# app.config_from_object(settings, namespace='CELERY')
app.conf.broker_url = 'amqp://localhost:5672'
app.conf.accept_content = ['application/json']
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'email_weekly': {
        'task': 'news.tasks.celery_send_weekly_mail',
        'schedule': crontab(0, 8, day_of_week=[1])

     },
 }
import datetime

from celery import shared_task
import time

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category

"""
Теория по модулю Д10
@shared_task
"""
@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

"""
Здесь мы использовали функцию sleep() из пакета time, чтобы остановить выполнение процесса на 10 секунд. 
Это поможет нам убедиться, что Клиент не «встал», пока выполняется эта задача.
"""

@shared_task
def celery_notify_subscribers(primary_key):
    instance = Post.objects.get(pk=primary_key)
    html_content = render_to_string('email/notification_on_create.html', {'new_post': instance}, )
    cats = instance.categorys.all()
    sendto_set = set()
    for cat in cats:
        sendto_set |= cat.get_subscribers_emails()
    msg = EmailMultiAlternatives(
        subject=f'"Здравствуйте, {instance.author.user}! Я брокер сообщений CELERY и у меня отличная новость!"',
        body=instance.text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=sendto_set)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task()
def celery_send_weekly_mail():
    from_date = datetime.datetime.now() - datetime.timedelta(days=7)

    for category in Category.objects.all():
        recent_posts = Post.objects.filter(categories=category).filter(creation_date__gte=from_date)
        if recent_posts.exists():
            html_content = render_to_string('account/email/weekly_mailing.html',
                                            {'posts': recent_posts,
                                             'categories': category}, )
            msg = EmailMultiAlternatives(
                subject=f'"На портале GoodNews новые статьи по тематике на которую вы подписаны! Успели прочитать?"',
                body="Список публикаций за неделю",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=category.get_subscribers_emails())
            msg.attach_alternative(html_content, "text/html")
            msg.send()
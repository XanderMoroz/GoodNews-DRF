import os
import random
from datetime import datetime


from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Author
from django.conf import settings


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Сигнал для привязки профиля к новому пользователю"""
    if created:
        random_number = random.randint(1, 6)
        random_avatar = f'images/avatars/default/{random_number}.png'
        author = Author.objects.create(user=instance,
                                       photo=random_avatar)
        author.save()

# @receiver(m2m_changed, sender=Post.categories.through)
# def notify_subscribers(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         html_content = render_to_string('blogs/email/send_mail.html', {'new_post': instance}, )
#         cats = instance.categories.all()
#         sendto_set = set()
#         # формируем список для рассылки
#         for cat in cats:
#             sendto_set = cat.get_subscribers_emails()
#         msg = EmailMultiAlternatives(
#             subject=f'"Здравствуйте, {instance.author.user} Новая статья в твоём любимом разделе!"',
#             body=f'{instance.text}',
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=sendto_set)
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()

@receiver(pre_save, sender=Post)
def check_post_limits(sender, instance, **kwargs):
    today_posts = Post.objects.filter(creation_date=datetime.now().date())
    return len(today_posts)
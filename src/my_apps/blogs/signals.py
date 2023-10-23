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
    """
    This signal is used to bind a profile to a new user.
    """
    if created:
        random_avatar = f'images/avatars/default/{random.randint(1, 6)}.png'
        Author.objects.create(user=instance, photo=random_avatar)

# @receiver(m2m_changed, sender=Post.categories.through)
# def notify_subscribers(sender, instance, action, **kwargs):
#     """
#     This function sends a notification to all subscribers when a post is added.
#     """
#     if action == 'post_add':
#         subscribers_emails = _get_subscribers_emails(instance.categories.all())
#         _send_email_notification(subscribers_emails, instance)

@receiver(pre_save, sender=Post)
def check_post_limits(sender, instance, **kwargs):
    """
    This function checks the limit for posts created in a day.
    """
    return Post.objects.filter(creation_date=datetime.now().date()).count()


def _get_subscribers_emails(categories):
    """
    This function returns a set of all subscriber email addresses for given categories.
    """
    sendto_set = set()
    for cat in categories:
        sendto_set = cat.get_subscribers_emails()
    return sendto_set

def _send_email_notification(emails, instance):
    """
    This function sends an email notification to a given set of email addresses.
    """
    html_content = render_to_string('blogs/email/send_mail.html', {'new_post': instance})
    msg = EmailMultiAlternatives(
        subject=f'"Hello, {instance.author.user} There is a new article in your favorite section!"',
        body=f'{instance.text}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
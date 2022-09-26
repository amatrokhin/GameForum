from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from django.contrib.auth.models import User
from datetime import date, timedelta

from .models import Post, Reply


@shared_task
def notify_receiver(pk):
    # select_related allow for less queries to DB by adding related fields to the initial query
    instance = Reply.objects.select_related('post__author', 'post').get(pk=pk)
    receiver = instance.post.author.email

    html_content = render_to_string(                             # convert and add context
        'mailing_new_reply.html',
        {
            'reply': instance,
            'post': instance.post,
        }
    )

    msg = EmailMultiAlternatives(                                # configure message
        subject='Ответ на ваш пост',
        body=instance.text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[receiver]
    )
    msg.attach_alternative(html_content, "text/html")  # attach html to message
    msg.send()


@shared_task
def notify_creator(pk):
    # select_related allow for less queries to DB by adding related fields to the initial query
    instance = Reply.objects.select_related('author', 'post').get(pk=pk)
    if instance.accepted:
        creator = instance.author.email

        html_content = render_to_string(                             # convert and add context
            'mailing_new_reply.html',
            {
                'reply': instance,
                'post': instance.post,
            }
        )

        msg = EmailMultiAlternatives(                                # configure message
            subject='Ваш отклик принят',
            body=instance.text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[creator]
        )
        msg.attach_alternative(html_content, "text/html")  # attach html to message
        msg.send()


@shared_task()
def weekly_update():                                             # email everybody about new posts every week
    week_ago = date.today() - timedelta(weeks=1)

    if Post.objects.filter(time_in__gte=week_ago).exists():      # if smth posted a week ago

        users = User.objects.all()

        html_content = render_to_string(                         # convert and add context
            'weekly_updates_mailing.html',
        )

        msg = EmailMultiAlternatives(                            # configure message
            subject='Новые посты за неделю',
            body=f'Обновления за неделю можно посмотреть по ссылке: '
                 f'http://127.0.0.1:8000/posts',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email for user in users]
        )

        msg.attach_alternative(html_content, "text/html")        # attach html to message
        msg.send()

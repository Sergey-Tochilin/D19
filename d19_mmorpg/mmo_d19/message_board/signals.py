from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Replay
from django.conf import settings


def send_notifications(preview, pk, title, subscribers_list):
#из списка подписчиков при каждой итерации цила отправляется сообщение 1 подписчику с обращением
#к конкретному подписчику в письме
    for s in subscribers_list:
        #получаю имя подписчика
        sub_name = s.username
        #получаю почту подписчика, она должна быть списком или словарем, что бы работало
        sub_email = [s.email]
        html_content = render_to_string(
            'post_created_email.html',
            {
                'title': title,
                'text': preview,
                'link': f'{settings.SITE_URL}/posts/post/{pk}',
                'sub_name': sub_name

            }
        )

        msg = EmailMultiAlternatives(
            subject='',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=sub_email,
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@receiver(m2m_changed, sender=Post)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        #Список подписчиков его передать в функцию для рассылки
        subscribers_list = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_list += [s for s in subscribers]

        send_notifications(instance.preview, instance.pk, instance.title, subscribers_list)


def send_new_replay(replay_author, replay_text, replay_post):

    html_content = render_to_string(
        template_name='replay_created_email.html',
        context={
            'post_author': replay_post.post_author,
            'replay_author': replay_author,
            'text': replay_text,
            'link': f'{settings.SITE_URL}/posts/post/{replay_post.id}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='У вашего объявления новый отклик!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[replay_post.post_author.email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#сигнал новый отклик
@receiver(post_save, sender=Replay)
def about_notify_new_replay(sender, instance, **kwargs):
    replay_author = instance.replay_author
    replay_text = instance.text
    replay_post = instance.post #получаю поле внешний ключ на модель постов

    send_new_replay(replay_author, replay_text, replay_post)


def send_accept_replay(replay_author, replay_post):
    html_content = render_to_string(
        template_name='accept_replay_email.html',
        context={
            'replay_author': replay_author,
            'link': f'{settings.SITE_URL}/posts/post/{replay_post.id}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Ваш отклик приняли!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[replay_author.email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#сигнал принятия отклика
@receiver(post_save, sender=Replay)
def about_notify_accept_replay(sender, instance, **kwargs):
    replay_author = instance.replay_author
    replay_post = instance.post #получаю поле внешний ключ на модель постов

    send_accept_replay(replay_author, replay_post)



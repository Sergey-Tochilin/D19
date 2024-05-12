from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Replay
from django.conf import settings

'''
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
                'text': preview,
                'link': f'{settings.SITE_URL}/posts/post/{pk}',
                'sub_name': sub_name

            }
        )

        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=sub_email,
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@receiver(m2m_changed, sender=)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        #Список подписчиков его передать в функцию для рассылки
        subscribers_list = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_list += [s for s in subscribers]

        send_notifications(instance.preview, instance.pk, instance.title, subscribers_list)
'''

def send_new_replay(pk, post_author, post_id, author_email, replay_author, replay_text):

    html_content = render_to_string(
        template_name='replay_created_email.html',
        context={
            'post_author': post_author,
            'replay_author': replay_author,
            'text': replay_text,
            'link': f'{settings.SITE_URL}/post/{post_id}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='У вашего поста новый отклик!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[author_email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#сигнал новый отклик
@receiver(post_save, sender=Replay)
def about_notify_new_replay(sender, instance, **kwargs):
    replay = Replay.objects.all()
    '''через instance(в ней содержится объект модели Replay) я хочу получить сделующие поля
    автора поста, по идее я через фильтр обращаюсь к к полю post модели Replay в котором внешний ключ на модель Post
    и там я уже обращаюсь к полю post-author
    не понимаю как добраться до полей связаных моделей, так не работает'''
    post_author = Replay.objects.filter('post__post_author')
    post_id = Replay.objects.filter('post__post_id')
    author_email = Replay.objects.filter('post__post_author__email')
    replay_author = replay.replay_author
    replay_text = replay.text

    send_new_replay(instance.pk, post_author, post_id, author_email, replay_author, replay_text)




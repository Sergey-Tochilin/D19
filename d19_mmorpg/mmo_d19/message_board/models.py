from django.db import models
from django.contrib.auth.models import User, AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)
    #нужно создавать до остальный моделей
class Category(models.Model):
    dd = 'ДД'
    tk = 'Танк'
    hl = 'Хил'
    tr = 'Торговец'
    gm = 'Гильдмастер'
    qg = 'Квестгивер'
    bs = 'Кузнец'
    tn = 'Кожевник'
    pm = 'Зельевар'
    sm = 'Мастер заклинаний'

    CATEGORY_TYPES = [
        (dd, 'DAMAGEDILLER'),
        (tk, 'TANK'),
        (hl, 'HEALER'),
        (tr, 'TRADER'),
        (gm, 'GILDMASTER'),
        (qg, 'QUESTGIVER'),
        (bs, 'BLACKSMITH'),
        (tn, 'TANNER'),
        (pm, 'POTIONMAKER'),
        (sm, 'SPELLMASTER'),
    ]

    name = models.CharField(max_length=17, choices=CATEGORY_TYPES)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = RichTextUploadingField()
    date = models.DateTimeField(auto_now=True)#обновляет метку каждый раз при изменении (сохранении) строки в базе
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    def preview(self):
        prew_text = self.text[0:124]
        return prew_text

    def __str__(self):
        return self.title.title()

    def get_absolute_url(self):
        return f'/posts/post/{self.id}'


class Replay(models.Model):
    replay_author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)# статус отклика по умолчанию False
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return f'/posts/profile'



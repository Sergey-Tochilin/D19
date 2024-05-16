from django import forms
from django.forms import ModelForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from allauth.account.forms import SignupForm
from string import hexdigits
import random

from django.conf import settings
from django.core.mail import send_mail

from .models import Post, Replay


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации',
            message=f'Код активации аккаунта: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return user

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
        ]
        widgets = {
            'text': CKEditorUploadingWidget(), #поле для загрузки файлов при помощи ckeditor
        }

class ReplayForm(ModelForm):
    class Meta:
        model = Replay
        fields = [
            'text',
        ]
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-text', 'cols': 100, 'rows': 4})
        }


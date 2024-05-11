from django_filters import FilterSet, DateFilter
from django import forms

from .models import Post, Replay


class PostFilter(FilterSet):
    date = DateFilter(
        widget=forms.DateInput(format='%d %m %Y', attrs={'type': 'date'}),
        field_name='date',
        lookup_expr='date__gte',
        label='Позже этой даты:'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'post_author': ['exact'],
            'category': ['exact']

        }

class UserPostFilter(FilterSet):

    class Meta:
        model = Replay
        fields = [
            'post'
        ]

    def __init__(self, *args, **kwargs):
        super(UserPostFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(post_author_id=kwargs.get('request'))

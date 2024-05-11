from django.urls import path
from .views import *
from allauth.account.views import LogoutView


urlpatterns = [
    path('', PostList.as_view(), name='posts_list'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/create/', PostCreate.as_view(), name='post_create'),
    #path('<int:pk>/replay/create/', ReplayCreate.as_view(), name='replay_create'),#передаю id поста для создания отклика
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
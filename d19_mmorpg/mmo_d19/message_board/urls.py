from django.urls import path
from .views import *
from allauth.account.views import LogoutView


urlpatterns = [
    path('', PostList.as_view(), name='posts_list'),
    path('category_list/', CategoryList.as_view(), name='category_list'),
    path('<int:pk>/category/subscribe/', subscribe, name='subscribe'), #тут скорее всего тоже ошибка
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/create/', PostCreate.as_view(), name='post_create'),
    path('post/create/<int:pk>', PostUpdate.as_view(), name='post_update'),
    #path('<int:pk>/replay/create/', ReplayCreate.as_view(), name='replay_create'),#передаю id поста для создания отклика
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accept_replay/<int:replay_id>', accept_replay, name='accept_replay'),#replay_id - id конкретного отклика
    path('delete_replay/<int:replay_id>', delete_replay, name='delete_replay'),


]
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import *
from .filters import PostFilter, UserPostFilter


# Create your views here.

class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, template_name='invalid_code.html')
        return redirect('account_login')

class PostList(ListView):
    model = Post

    template_name = 'all_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    queryset = Post.objects.all().order_by('-date')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        if self.request.GET:
            return self.filterset.qs
        return Post.objects.all().order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class CategoryList(ListView):
    model = Category

    template_name = 'all_categories.html'
    context_object_name = 'categories'
    paginate_by = 10


#оформить подписку
@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return redirect('category_list')

#отменить подписку
@login_required()
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    return redirect('category_list')



class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replay_form'] = ReplayForm()
        return context

    # Добавляю метод с формой на страницу
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = ReplayForm(request.POST)
        if form.is_valid():
            replay = form.save(commit=False)
            replay.post = post
            replay.replay_author = request.user
            replay.save()
            return redirect('post_detail', pk=post.pk)





'''
class ReplayCreate(LoginRequiredMixin, CreateView):
    model = Replay
    form_class = ReplayForm
    template_name = 'replay_create.html'


    def form_valid(self, form):
        replay = form.save(commit=False) #сохраняю объект без сохранения в БД
        replay.replay_author = self.request.user
        replay.post_id = self.kwargs['pk']#Передаю id поста, к которому создавать отклик
        replay.save()
        return super().form_valid(form)'''




class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    #Для автоматического заполнения поля автор авторизованным пользователем
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_author = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_update.html'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        #Переопределяю контекстный словать
        context = super().get_context_data(**kwargs)
        #pk я получаю из ссылки <int:pk> он передается в kwargs
        #это пост, который будет редактироваться и в нем я получаю автора поста
        context['post_author'] = Post.objects.get(pk=self.kwargs.get('pk')).post_author
        return context



class PostSearch(ListView):
    model = Post
    ordering = '-date'
    template_name = 'post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        if self.request.GET:
            return self.filterset.qs
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

class ProfileView(LoginRequiredMixin, ListView):
    model = Replay
    template_name = 'profile.html'
    context_object_name = 'replays'#Так как переопределил кверисет нужна контекстная переменная в которой он лежит
    def get_queryset(self):
        queryset = Replay.objects.filter(post__post_author_id=self.request.user.id).order_by('-date')
        self.filterset = UserPostFilter(self.request.GET, queryset=queryset, request=self.request.user.id)
        if self.request.GET:
            return self.filterset.qs
        return Replay.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

def accept_replay(request, replay_id):
    replay = get_object_or_404(Replay, pk=replay_id)# передаю модель и pk по id
    replay.status = True
    replay.save()
    return redirect(reverse('profile'))#возвращаюсь обратно

def delete_replay(request, replay_id):
    replay = get_object_or_404(Replay, pk=replay_id)
    replay.delete()
    return redirect(reverse('profile'))



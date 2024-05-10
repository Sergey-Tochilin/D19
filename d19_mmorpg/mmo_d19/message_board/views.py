from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


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





class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'






class ReplayCreate(LoginRequiredMixin, CreateView):
    model = Replay
    form_class = ReplayForm
    template_name = 'replay_create.html'


    def form_valid(self, form):
        replay = form.save(commit=False)
        replay.replay_author = self.request.user
        replay.post_id = self.kwargs['pk']#Передаю id поста, к которому создавать отклик
        replay.save()
        return super().form_valid(form)


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
    form_class = PostForm
    template_name = 'post_create.html'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

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
    context_object_name = 'replays'

    def get_queryset(self):
        queryset = Replay.objects.filter(post__post_author_id=self.request.user.id)
        self.filterset =UserPostFilter(self.request.GET, queryset=queryset, request=self.request.user.id)
        if self.request.GET:
            return self.filterset.qs
        return Replay.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
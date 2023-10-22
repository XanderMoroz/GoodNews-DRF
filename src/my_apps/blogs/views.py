import os
from datetime import datetime

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchHeadline
from django.contrib.postgres.search import TrigramSimilarity

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import CreateView, FormMixin

from .forms import PostForm, CategoryForm, CommentForm
from .models import Post, Category, Author, PostCategory, Comment  # импорт нашей модели
from .filters import PostFilter  # импорт нашего фильтра
from .signals import check_post_limits

class MainView(TemplateView):
    template_name = 'blogs/main.html'

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим пользователя'.
        user = self.request.user
        # Добавим в контекст случайную статью
        main_post = Post.objects.order_by('?').first()
        context['main_post'] = main_post
        # Добавим в контекст еще две случайных статьи
        secondary_post1 = Post.objects.order_by('?').first()
        context['secondary_post1'] = secondary_post1
        post_cat1 = PostCategory.objects.filter(post=secondary_post1)
        context['post_cat1'] = post_cat1
        secondary_post2 = Post.objects.order_by('?').first()
        context['secondary_post2'] = secondary_post2
        post_cat2 = PostCategory.objects.filter(post=secondary_post2)
        context['post_cat2'] = post_cat2
        # Добавим в контекст еще несколько свежих статей
        all_latest_posts = Post.objects.order_by('creation_date')
        latest_posts = all_latest_posts[:4]
        context['latest_posts'] = latest_posts

        list_of_categories = Category.objects.all()
        context['list_of_categories'] = list_of_categories

        return context


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post_list'
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-creation_date'
    # поставим постраничный вывод в десять элемент
    paginate_by = 1
    # добавляем форм класс, чтобы получать доступ к форме через метод POST
    form_class = PostForm

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # вписываем наш фильтр (PostFilter) в контекст
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        # context['form'] = PostForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=queryset).qs

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, вносим в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новeую статью
            form.save()

        return super().get(request, *args, **kwargs)


class Search(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'blogs/post_search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'search_list'
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-creation_date'
    # поставим постраничный вывод в десять элемент
    paginate_by = 10

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # Добавим результаты поиска
        user_search_request = self.request.GET.get("query")

        if user_search_request:
            # search_res = Post.objects.all()
            search_res = Post.objects.annotate \
                (similarity=TrigramSimilarity \
                    ('title', user_search_request), ).filter \
                (similarity__gt=0.3).order_by('-similarity')
        else:
            search_res = None
        print(search_res)
        context['search_res'] = search_res
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=queryset).qs


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной публикации
    model = Post
    # Используем другой шаблон — post_detail.html
    template_name = 'blogs/post_detail.html'
    # Название объекта, в котором будет выбранная пользователем публикация
    context_object_name = 'post_detail'
    # form_class = CommentForm



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # current_user = self.request.user
        # if current_user is not None:
        #     current_author = Author.objects.filter(user=current_user).first()
        #     context['current_author'] = current_author
        # Добавим к публикации комментарии.
        post_id = self.kwargs.get('pk')
        comments = Comment.objects.filter(post=post_id)
        context['comments'] = comments
        # Добавим аватары к комментариям.
        comments = Comment.objects.all()
        avatar_dict = {}
        comment_users = [comment.user for comment in comments]
        for user in comment_users:
            author_user = Author.objects.filter(user=user).first()
            avatar_dict[user.id] = author_user.photo
        context['avatar_dict'] = avatar_dict
        # Добавим похожие публикации.
        similar_posts = []
        cur_post_categories = PostCategory.objects.filter(post=post_id)
        for post_categories in cur_post_categories:
            similar_posts.append(post_categories.post)
        context['similar_posts'] = similar_posts
        return context


class PostCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Класс представления для создания статьи.
    Наследован от встроенного дженерика, миксина требующего авторизацию и миксина, требующего право доступа
    """
    permission_required = ('news.add_post',)
    template_name = 'blogs/cruds/create_post.html'
    form_class = PostForm

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        author = Author.objects.get(user_id=user.pk)
        initial['author'] = author
        return initial

    def post(self, request, *args, **kwargs):
        new_post = Post(
            type=request.POST['type'],
            text=request.POST['text'],
            title=request.POST['title'],
            author_id=request.POST['author'],
                        )
        if check_post_limits(sender=Post, instance=new_post, **kwargs) < 3:
            new_post.save()
            new_post.categories.add(request.POST.get('categories'))

        return redirect('main')


class PostUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Класс представления для редактирования статьи.
    Наследован от встроенного дженерика, миксина требующего авторизацию и миксина, требующего право доступа
    """
    permission_required = ('news.change_post',)
    template_name = 'blogs/cruds/edit_post.html'
    form_class = PostForm


    def get_object(self, **kwargs):
        """
        метод get_object мы используем вместо queryset, чтобы получить информацию об объекте,
        который мы собираемся редактировать
        :param kwargs:
        :return: объект класса Post
        """
        post_id = self.kwargs.get('pk')
        return Post.objects.get(pk=post_id)

class PostDeleteView(DeleteView):
    """
    Класс представления для удаления статьи.
    Наследован от встроенного дженерика.
    """
    template_name = 'blogs/cruds/delete_post.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('profile')

@login_required
def subscribe(request, **kwargs):
    category = Category.objects.get(pk=kwargs['pk'])
    user = request.user
    if user not in category.subscribers.all():
        category.subscribers.add(user)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def unsubscribe(request, **kwargs):
    category = Category.objects.get(pk=kwargs['pk'])
    user = request.user
    if user in category.subscribers.all():
        category.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER', '/'))


class CategoriesSubscription(ListView, FormMixin):
    model = Category
    template_name = 'blogs/subscription.html'
    context_object_name = 'subscription'
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_of_categories = Category.objects.all()
        context['list_of_categories'] = list_of_categories
        post_dict = {}
        for cat in list_of_categories:
            posts_of_category = PostCategory.objects.filter(category=cat)
            post_dict[cat.title] = posts_of_category.count()
        context['post_dict'] = post_dict

        return context


class PostsOfCategory(ListView):
    model = Post
    template_name = 'blogs/posts_of_category.html'
    context_object_name = 'posts_of_category'
    ordering = '-creation_date'
    paginate_by = 1

    def get_queryset(self):
        category_id = self.kwargs['pk']
        category = Category.objects.get(id=category_id)
        queryset = super().get_queryset()
        return queryset.filter(categories=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        current_category = Category.objects.get(id=category_id)
        context['current_category'] = current_category
        return context

class CommentCreateView(CreateView, LoginRequiredMixin):
    """
    Класс представления для создания статьи.
    Наследован от встроенного дженерика, миксина требующего авторизацию и миксина, требующего право доступа
    """
    # permission_required = ('news.add_post',)
    template_name = 'blogs/cruds/create_comment.html'
    form_class = CommentForm

    def get_initial(self):
        initial = super().get_initial()
        # Добавим автора комментария
        current_user = self.request.user
        initial['user'] = current_user
        # Добавим публикация, которую комментируем
        comment_post = Post.objects.get(id=self.kwargs['pk'])
        initial['post'] = comment_post
        # Добавим текст комментария
        comment_text = "This article is awesome!"
        initial['text'] = comment_text

        return initial

    def post(self, request, *args, **kwargs):
        new_post = Post(
            type=request.POST['type'],
            text=request.POST['text'],
            title=request.POST['title'],
            author_id=request.POST['author'],
                        )
        if check_post_limits(sender=Post, instance=new_post, **kwargs) < 3:
            new_post.save()
            new_post.categories.add(request.POST.get('categories'))

        return redirect('main')
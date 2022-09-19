from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import CreateView, FormMixin
from .forms import PostForm, CategoryForm
from .models import Post, Category, Author  # импорт нашей модели
from .filters import PostFilter  # импорт нашего фильтра
from .signals import check_post_limits


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
    template_name = 'search.html'
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
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # вписываем наш фильтр (PostFilter) в контекст
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=queryset).qs


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной публикации
    model = Post
    # Используем другой шаблон — post_detail.html
    template_name = 'news/post_detail.html'
    # Название объекта, в котором будет выбранная пользователем публикация
    context_object_name = 'post_detail'

class PostCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Класс представления для создания статьи.
    Наследован от встроенного дженерика, миксина требующего авторизацию и миксина, требующего право доступа
    """
    permission_required = ('news.add_post',)
    template_name = 'news/add.html'
    form_class = PostForm

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        author = Author.objects.get(user_id=user.pk)
        initial['author'] = author
        return initial

    def post(self, request, *args, **kwargs):
        new_post = Post(
            post_type=request.POST['post_type'],
            post_text=request.POST['post_text'],
            post_title=request.POST['post_title'],
            author_id=request.POST['author'],
                        )
        if check_post_limits(sender=Post, instance=new_post, **kwargs) < 3:
            new_post.save()
            new_post.categories.add(request.POST.get('categories'))

        return redirect('news')

    """
        send_mail(
            subject=f'"Здравствуйте, {new_post.author.user} Новая статья в твоём любимом разделе!"',
            # сообщение с кратким описанием проблемы
            message=new_post.post_text[:50] + "...",
            # здесь указываете почту, с которой будете отправлять (об этом попозже)
            from_email='GoodNewsObserver@yandex.ru',
            recipient_list=['GoodNewsObserver@yandex.ru']) 
        return redirect('add')
    """

class PostUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Класс представления для редактирования статьи.
    Наследован от встроенного дженерика, миксина требующего авторизацию и миксина, требующего право доступа
    """
    permission_required = ('news.change_post',)
    template_name = 'news/add.html'
    form_class = PostForm


    def get_object(self, **kwargs):
        """
        метод get_object мы используем вместо queryset, чтобы получить информацию об объекте,
        который мы собираемся редактировать
        :param kwargs:
        :return: объект класса Post
        """
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    """
    Класс представления для удаления статьи.
    Наследован от встроенного дженерика.
    """
    template_name = 'news/delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

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


class CategoriesSubscription(LoginRequiredMixin, ListView, FormMixin):
    model = Category
    template_name = 'news/subscription.html'
    context_object_name = 'subscription'
    form_class = CategoryForm

    def get_context_data(self,
                         **kwargs):
        context = super().get_context_data(**kwargs)
        return context
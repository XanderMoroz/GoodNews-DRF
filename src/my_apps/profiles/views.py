from datetime import datetime

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, UpdateView

from src.my_apps.blogs.models import Author, Post, UserCategory
from src.my_apps.profiles.forms import ProfileForm


# Create your views here.

class SignupView(View):
    
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'profiles/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # перенаправьте на страницу входа после успешной регистрации
        else:
            return render(request, 'profiles/signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'profiles/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  # перенаправьте на вашу домашнюю страницу после успешного входа
            else:
                # обработка ошибки входа
                return render(request, 'profiles/login.html', {'form': form, 'error': 'Неправильное имя пользователя или пароль'})
        else:
            return render(request, 'profiles/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main')  # перенаправьте на вашу домашнюю страницу после выхода


class Profile(TemplateView):
    """Представление профиля пользователя."""
    model = User                                        # Имя модели
    template_name = 'profiles/profile.html'              # Относительный адрес шаблона

    def get_initial(self):
        """Переопределение функции для автозаполнения поля 'user' """
        initial = super().get_initial()
        user = self.request.user
        initial['user'] = user
        return initial

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        # Добавим в контекст профиль пользователя
        profile = Author.objects.get(user=current_user)
        context['profile'] = profile
        author_posts = Post.objects.filter(author=profile)
        context['author_posts'] = author_posts
        # Добавим список категорий на которые подписан пользователь.
        user_cats = UserCategory.objects.filter(user=current_user)
        category_subscribed = [user_cat.category for user_cat in user_cats]
        context['category_subscribed'] = category_subscribed
        # Добавим время с момента регистрации.
        # start_time = current_user.date_joined
        # end_time = datetime.now()
        # time_on_site = end_time - start_time
        context['date_now'] = datetime.now()

        return context

class EditProfile(UpdateView):
    """Представление для редактирования профиля пользователя."""
    template_name = 'profiles/edit_profile.html'         # Относительный адрес шаблона
    form_class = ProfileForm                            # Имя формы
    context_object_name = 'current_profile'

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        current_user = self.request.user
        # id = self.kwargs.get('pk')
        return Author.objects.get(user=current_user)

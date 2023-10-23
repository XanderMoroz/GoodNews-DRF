from datetime import datetime

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, UpdateView

from src.my_apps.blogs.models import Author, Post, UserCategory
from src.my_apps.profiles.forms import ProfileForm


class FormView(View):
    """
    Base class for views that handle forms.
    """
    form_class = None
    template_name = None

    def get(self, request):
        """
        Handles GET requests and renders the form.
        """
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Handles POST requests and processes the form data.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        """
        Method to be implemented in subclasses to handle valid form submission.
        """
        raise NotImplementedError

class SignupView(FormView):
    """
    View for user registration/signup.
    """
    form_class = UserCreationForm
    template_name = 'profiles/signup.html'

    def form_valid(self, form):
        """
        Saves the user registration form data and redirects to login page.
        """
        form.save()
        return redirect('login')

class LoginView(FormView):
    """
    View for user login.
    """
    form_class = AuthenticationForm
    template_name = 'profiles/login.html'

    def form_valid(self, form):
        """
        Authenticates user credentials and logs in the user.
        Redirects to the user's profile page upon successful login.
        """
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('profile')
        else:
            return render(
                self.request,
                'profiles/login.html',
                {
                    'form': form,
                    'error': 'Invalid username or password'})

class LogoutView(View):
    """
    View for user logout.
    """
    def get(self, request):
        """
        Logs out the user and redirects to the main page.
        """
        logout(request)
        return redirect('main')

class Profile(TemplateView):
    """
    View for displaying user profile.
    """
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to be used in the template.
        """
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        profile = Author.objects.get(user=current_user)
        context.update({
            'profile': profile,
            'author_posts': Post.objects.filter(author=profile),
            'category_subscribed': [user_cat.category for user_cat in UserCategory.objects.filter(user=current_user)],
            'date_now': datetime.now(),
        })
        return context

class EditProfile(UpdateView):
    """
    View for editing user profile.
    """
    template_name = 'profiles/edit_profile.html'
    form_class = ProfileForm
    context_object_name = 'current_profile'

    def get_object(self, **kwargs):
        """
        Retrieves the current user's profile object.
        """
        return Author.objects.get(user=self.request.user)
from django.urls import path
from .views import IndexView

urlpatterns = [
    path('profile', IndexView.as_view()),
]
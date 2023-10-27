from django.urls import path

from .views import (
    SignupView,
    login_view, # LoginView,
    LogoutView,
    Profile,
    EditProfile,
)

# handler404 = "app.views.handler404"
# handler500 = "app.views.handler500"

urlpatterns = [
    # Auth Views
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Profile Views
    path('profile/', Profile.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', EditProfile.as_view(), name='edit_profile'),
]

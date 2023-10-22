from django.urls import path
from .views import (SignupView,
                    LoginView,
                    LogoutView,
                    Profile,
                    EditProfile)

# handler404 = "app.views.handler404"
# handler500 = "app.views.handler500"

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', Profile.as_view(), name='profile'),
    path('edit/<int:pk>', EditProfile.as_view(), name='edit_profile'),
]
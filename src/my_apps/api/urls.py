import tomllib

from django.urls import include, path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from . import views
from .views import AuthorViewSet, CreateUserView

with open(f"pyproject.toml", "rb") as f:
    DRF_PROJECT_CONTENT = tomllib.load(f)["tool"]["poetry"]

schema_view = get_schema_view(
    openapi.Info(
        title=DRF_PROJECT_CONTENT["name"],
        default_version=DRF_PROJECT_CONTENT["version"],
        description=DRF_PROJECT_CONTENT["description"],
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="moroz070688@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)

urlpatterns = [
    # DOCS URLS
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # SIGN-UP NEW USER
    path("users/sign_up", views.UserCreate.as_view(), name="sign_up"),

    # AUTHENTICATE USER BY JWT TOKEN
    path("auth_by_jwt_token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "auth_by_jwt_token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("auth_by_jwt_token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # USER MANAGEMENT
    path("users/user_list/", views.UserList.as_view(), name="user_list"),
    path("users/<int:pk>", views.UserDetail.as_view(), name="user_detail"),
    path("users/<int:pk>/update", views.UserUpdate.as_view(), name="user_update"),
    path("users/<int:pk>/delete", views.UserDelete.as_view(), name="user_delete"),

    path('', include(router.urls)),

    # POST MANAGEMENT
    path("posts/", views.PostList.as_view(), name="posts"),
    path("posts/<int:pk>", views.PostDetail.as_view()),
    path('', include(router.urls)),

    # COMMENTS MANAGEMENT
    path("comments/", views.CommentList.as_view()),
    path("comments/<int:pk>", views.CommentDetail.as_view()),

    # CATEGORIES MANAGEMENT
    path("categories/", views.CategoryList.as_view()),
    path("categories/<int:pk>/", views.CategoryDetail.as_view()),
]
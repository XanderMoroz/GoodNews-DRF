from django.urls import path

from .views import (
    MainView,
    PostDetail,
    Search,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,

    subscribe,
    unsubscribe,

    CategoriesSubscription,
    PostsOfCategory
)

urlpatterns = [
    # Main and List Views
    path('', MainView.as_view(), name='main'),

    # Post CRUD operations
    path('create', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('edit/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),

    # Search
    path('search', Search.as_view(), name='search'),

    # Comments
    path('<int:post_id>/comment_create', CommentCreateView.as_view(), name='comment_create'),

    # Subscriptions
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name='unsubscribe'),
    path('subscription/', CategoriesSubscription.as_view(), name='subscription'),

    # Categories
    path('category/<int:pk>/posts', PostsOfCategory.as_view(), name='posts_of_categories'),
]
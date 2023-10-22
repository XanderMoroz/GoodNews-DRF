from django.contrib import admin
from django.urls import path
from .views import (PostList,
                    PostDetail,
                    Search,
                    PostCreateView,
                    PostDeleteView,
                    PostUpdateView,
                    subscribe,
                    unsubscribe,
                    CategoriesSubscription,
                    MainView, PostsOfCategory, CommentCreateView)

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('post_list', PostList.as_view(), name='post_list'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    # добавим путь
    path('search', Search.as_view(), name='search'),
    path('create', PostCreateView.as_view(), name='post_create'),
    path('edit/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/comment_create', CommentCreateView.as_view(), name='comment_create'),

    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name='unsubscribe'),
    path('subscription/', CategoriesSubscription.as_view(), name='subscription'),
    path('category/<int:pk>/posts', PostsOfCategory.as_view(), name='posts_of_categories'),


]

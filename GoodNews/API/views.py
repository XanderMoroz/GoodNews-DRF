from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    AuthorSerializer,
    PostSerializer,
    CategorySerializer)
from news.models import Author, Post, Category

# Create your views here.

class AuthorListCreateAPIView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # Добавим разрешение позволяющее создавать объект только админам сайта
    permission_classes = (IsAdminOrReadOnly,)


class AuthorUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # Добавим разрешение позволяющее создавать объект только админам сайта
    permission_classes = (IsAdminOrReadOnly,)


class PostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Добавим разрешение позволяющее создавать объект только авторизованным пользователям
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PostUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Добавим разрешение позволяющее редактировать объект только владельцу
    permission_classes = (IsOwnerOrReadOnly,)

class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # Добавим разрешение позволяющее создавать объект только админам сайта
    permission_classes = (IsAdminOrReadOnly,)


class CategoryUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # Добавим разрешение позволяющее менять и удалять объект только админу сайта
    permission_classes = (IsAdminOrReadOnly,)

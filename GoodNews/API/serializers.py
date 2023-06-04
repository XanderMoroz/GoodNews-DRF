from rest_framework import serializers
from django.contrib.auth.models import User
from news.models import Author, Post, Category, UserCategory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',) #'__all__'


class AuthorSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)

    class Meta:
        model = Author
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('author',
                  'post_type',
                  'categories',
                  'post_title',
                  'post_text',
                  ) #'__all__'



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


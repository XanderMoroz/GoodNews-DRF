from django.contrib.auth import get_user_model
from rest_framework import serializers

from src.my_apps.blogs.models import Author, Post, Comment, Category

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ("id", "username", "password", )


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Post
        fields = ["id",
                  "title",
                  "type",
                  "text",
                  "author",
                  "creation_date",
                  "categories",
                  ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.user.email")

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "post"]


class CategorySerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "title", "posts"]




from django import forms
from django.forms import ModelForm
from .models import Post, Category, Comment


# Создаём модельную форму
class PostForm(ModelForm):
    categories = forms.CheckboxSelectMultiple()

    class Meta:
        """
        В класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля.
        Мы уже делали что-то похожее с фильтрами.
        """
        model = Post
        fields = [
            'type',
            'title',
            'text',
            'categories',
            'author'
                ]
        labels = {
            'categories': "категории",
        }

        widgets = {'author': forms.HiddenInput()}


class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['title']


class CommentForm(ModelForm):

    class Meta:
        model = Comment

        fields = [
            'user', 'post', 'text'
        ]
        widgets = {
            'user': forms.HiddenInput(),
            'post': forms.HiddenInput(),
                   }

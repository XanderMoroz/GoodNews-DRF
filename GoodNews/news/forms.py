from django import forms
from django.forms import ModelForm
from .models import Post, Category


# Создаём модельную форму
class PostForm(ModelForm):
    #check_box = BooleanField(label='Confirm changes')



    class Meta:
        """
        В класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля.
        Мы уже делали что-то похожее с фильтрами.
        """
        model = Post
        fields = [
            'post_type',
            'post_title',
            'post_text',
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
        fields = ['category_name']
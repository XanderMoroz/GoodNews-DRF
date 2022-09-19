from django import forms
from django.forms import ModelForm
from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):
    #check_box = BooleanField(label='Confirm changes')
    class Meta:
        """
        В класс мета, как обычно, надо написать модель, по которой будет строиться формаи нужные нам поля.
        Мы уже делали что-то похожее с фильтрами.
        """
        model = Post
        fields = ['post_type',
                  'post_title',
                  'post_text',
                  #'categories',
                  'author'
                ]
        #widgets = {'author': forms.HiddenInput()}
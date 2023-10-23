from django import forms
from django.forms import ModelForm
from .models import Post, Category, Comment


class PostForm(ModelForm):
    """
    A model form built based on the Post model.
    Like filters, this form also requires specifying
    the model and the necessary fields.
    """
    categories = forms.CheckboxSelectMultiple()

    class Meta:
        model = Post
        fields = ['type', 'title', 'text', 'categories', 'author']
        labels = {'categories': "категории"}
        widgets = {'author': forms.HiddenInput()}


class CategoryForm(ModelForm):
    """
    A model form built based on the Category model.
    """
    class Meta:
        model = Category
        fields = ['title']


class CommentForm(ModelForm):
    """
    A model form built based on the Comment model.
    """
    class Meta:
        model = Comment
        fields = ['user', 'post', 'text']
        widgets = {
            'user': forms.HiddenInput(),
            'post': forms.HiddenInput(),
        }
from django import forms

from src.my_apps.blogs.models import Author


class ProfileForm(forms.ModelForm):
    """Форма для редактирования профиля"""

    class Meta:
        model = Author
        fields = ['user', 'photo',]
        labels = {'photo': "Ваш аватар",}
        widgets = {'user': forms.HiddenInput(),}
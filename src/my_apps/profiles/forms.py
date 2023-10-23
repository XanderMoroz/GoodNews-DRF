from django import forms
from src.my_apps.blogs.models import Author


class ProfileForm(forms.ModelForm):
    """
    Form for editing profile
    """
    class Meta:
        model = Author
        fields = ['user', 'photo']
        labels = {'photo': "Ваш аватар"}
        widgets = {'user': forms.HiddenInput()}
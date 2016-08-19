from django import forms
from django.contrib.auth.models import User

from movies.models import Rater


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class RaterForm(forms.ModelForm):
    class Meta:
        model = Rater
        exclude = ['user']

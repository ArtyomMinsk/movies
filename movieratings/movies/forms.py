from django import forms
from django.contrib.auth.models import User
from .models import Rater, Movie, Rating


# class RatingForm(forms.ModelForm):
#     class Meta:
#         model = Rating
#         fields = ('rating', 'review')


class RaterForm(forms.ModelForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = Rater
        fields = ['age', 'gender', 'occupation', 'zip_code']

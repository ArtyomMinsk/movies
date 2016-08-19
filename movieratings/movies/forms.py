from django import forms
from django.contrib.auth.models import User
from .models import Rater, Movie, Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating', 'review')

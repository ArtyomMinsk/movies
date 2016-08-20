from django import forms

from .models import Rater, Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'review']
        error_messages = {
            'required': 'This field is required!',
            'max_value': 'Please select an integer between 1 and 5',
            'min_value': 'Please select an integer between 1 and 5',
        }


class RaterForm(forms.ModelForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = Rater
        fields = ['age', 'gender', 'occupation', 'zip_code', ]
        error_messages = {
            'max_length': 'Too long!',
            'min_length': 'Too short!',
            'required': 'This field is required!'
        }

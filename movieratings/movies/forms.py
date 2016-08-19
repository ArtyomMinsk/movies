from django import forms

from movies.models import Rater


class RaterForm(forms.ModelForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = Rater
        fields = ['age', 'gender', 'occupation', 'zip_code']

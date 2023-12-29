from django import forms 
from .models import ReviewRating


class ReviewForm(forms.ModelForm):
    class Meta:
        models=ReviewRating
        fields=['subject','review','rating']
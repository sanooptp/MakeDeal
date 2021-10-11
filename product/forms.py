from django import forms
from django.contrib.auth import models
from django.forms import ModelForm
from django.utils.regex_helper import flatten_result
from .models import Product

class CreateProductForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # price = forms.NumberInput(attrs={'class': 'form-control'})
    image2 = forms.ImageField(required=False)
    image3 = forms.ImageField(required=False)
    image4 = forms.ImageField(required=False)
    time_to_publish = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),required=False)

    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['user']

class EditProductForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # price = forms.NumberInput(attrs={'class': 'form-control'})
    image2 = forms.ImageField(required=False)
    image3 = forms.ImageField(required=False)
    image4 = forms.ImageField(required=False)
    time_to_publish = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),required=False)
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['user']  
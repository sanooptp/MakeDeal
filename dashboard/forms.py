from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.db.models import fields
from django.db.models.fields.files import ImageFieldFile
from django.forms.fields import ImageField
from .models import UserDetails
from django.core.exceptions import ValidationError


 
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields =  ('username', 'email', 'password1','password2')


class UserDetailsForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # profile_picture = forms.ImageField(attrs={'class': 'form-control'})

    class Meta:
        profile_picture = forms.ImageField(required=False)
        model = UserDetails
        fields = ('name', 'phone', 'profile_picture')

        

class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email')
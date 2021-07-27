from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserDetails
from django.core.exceptions import ValidationError
 
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields =  ('username', 'email', 'password1','password2')


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ('name', 'phone')
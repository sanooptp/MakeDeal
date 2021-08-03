from django.db import models
from purchase.models import Purchase
from django import forms
from django.forms.models import ModelForm
from .models import Purchase

class BuyForm(ModelForm):
    class Meta:
        model = Purchase
        exclude = ['seller','buyer','status','product']
from django.db import models
from django.db.models import fields
from purchase.models import Purchase
from django import forms
from django.forms.models import ModelForm
from .models import Purchase

class BuyForm(ModelForm):
    class Meta:
        model = Purchase
        exclude = ['seller','buyer','status','product']

class PurchaseStatusForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['status']
        exclude = ['seller','buyer','product']
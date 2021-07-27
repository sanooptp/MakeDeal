from django.contrib.auth import models
from django.forms import ModelForm
from .models import Product

class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
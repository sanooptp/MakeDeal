from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserDetails(models.Model):
    user = models.OneToOneField(User, verbose_name=("user"), on_delete=models.CASCADE)
    name = models.CharField( max_length=50)
    phone = models.IntegerField()
    email = models.EmailField( max_length=254)


from django.db import models
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    category = models.CharField( max_length=50)

    def __str__(self):
        return self.category


class Product(models.Model):
    user = models.ForeignKey(User, verbose_name='', on_delete=models.CASCADE)
    name = models.CharField( max_length=50)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, verbose_name='', on_delete=models.CASCADE)
    location = models.CharField( max_length=50)
    image1 = models.ImageField( upload_to= 'images', height_field=None, width_field=None, max_length=None)
    image2 = models.ImageField( upload_to= 'images', height_field=None, width_field=None, max_length=None)
    image3 = models.ImageField( upload_to= 'images', height_field=None, width_field=None, max_length=None)
    image4 = models.ImageField( upload_to= 'images', height_field=None, width_field=None, max_length=None)
    price = models.IntegerField()
    time_to_publish = models.TimeField( auto_now= False, auto_now_add= False)
    

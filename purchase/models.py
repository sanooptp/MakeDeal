from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Purchase(models.Model):
    seller = models.ForeignKey(User, verbose_name=(""), on_delete=models.CASCADE, related_name= 'seller')
    buyer = models.ForeignKey(User, verbose_name=(""), on_delete=models.CASCADE, related_name='buyer')
    product = models.ForeignKey(Product, verbose_name=(""), on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    buyer_price = models.IntegerField()

    def __str__(self):
        return self.buyer.username
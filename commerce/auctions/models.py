from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionItems(models.Model):
    prdct_name = models.CharField(max_length=64)
    prdct_desc = models.CharField(max_length=200)
    prdct_price = models.FloatField()
    prdct_img = models.URLField(max_length=90)
    prdct_owner = models.ForeignKey('User', on_delete=models.CASCADE, default='1')

class Comments(models.Model):
    comment = models.CharField(max_length=300)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('AuctionItems', on_delete=models.CASCADE)
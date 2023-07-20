from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64, null=True, blank=True)

class AuctionItems(models.Model):
    prdct_name = models.CharField(max_length=64)
    prdct_desc = models.CharField(max_length=200)
    prdct_price = models.FloatField()
    prdct_img = models.URLField(max_length=90)
    prdct_owner = models.ForeignKey('User', on_delete=models.CASCADE, default='1')
    prdct_category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    creation_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

class Bids(models.Model):
    bid_amount = models.FloatField()
    bidded_item = models.ForeignKey('AuctionItems', on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey('User', on_delete=models.CASCADE)

class Comments(models.Model):
    comment = models.CharField(max_length=300)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('AuctionItems', on_delete=models.CASCADE)

class WatchList(models.Model):
    products = models.ManyToManyField(AuctionItems, null=True, blank=True)
    account_owner = models.ForeignKey('User', on_delete=models.CASCADE)
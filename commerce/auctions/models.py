from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionItems(models.Model):
    prdct_name = models.CharField(max_length=64)
    prdct_desc = models.CharField(max_length=200)
    prdct_price = models.FloatField()
    prdct_img = models.URLField(max_length=90)
from django.contrib import admin
from .models import User, AuctionItems

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionItems)
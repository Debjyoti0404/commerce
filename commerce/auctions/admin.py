from django.contrib import admin
from .models import User, AuctionItems, Comments

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionItems)
admin.site.register(Comments)
from django.contrib import admin
from .models import User, AuctionItems, Comments, WatchList

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionItems)
admin.site.register(Comments)
admin.site.register(WatchList)
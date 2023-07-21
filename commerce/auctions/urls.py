from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.category, name="categories"),
    path("categories/<str:name>", views.category_name, name="category_name"),
    path("closebid/<int:product_id>", views.closebid, name="closebid"),
    path("create", views.create_item, name="create"),
    path("listings/<int:product_id>", views.listings, name="listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("updatewatchlist/<int:product_id>", views.update_watchlist, name="updatewatchlist"),
    path("watchlist", views.watchlist, name="watchlist")
]

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, AuctionItems, Comments, WatchList
from .forms import CommentForm, ProductForm


@login_required
def create_item(request):
    if request.method == "POST":
        form_content = ProductForm(request.POST)
        if form_content.is_valid():
            product_name = form_content.cleaned_data['prdct_name']
            product_description = form_content.cleaned_data['prdct_desc']
            product_price = form_content.cleaned_data['prdct_price']
            product_image = form_content.cleaned_data['prdct_img']
            product_owner = User.objects.get(username = request.user.username)

            new_item = AuctionItems(
                prdct_name = product_name,
                prdct_desc = product_description,
                prdct_price = product_price,
                prdct_img = product_image,
                prdct_owner = product_owner
            )
            new_item.save()

        return HttpResponseRedirect(reverse("index"))
    
    else:
        product_form = ProductForm()
        return render(request, "auctions/create-listing.html", {
            "product_form" : product_form
        })


def index(request):
    all_auctionitem = AuctionItems.objects.all()
    return render(request, "auctions/index.html", {
        "all_auctionitems" : all_auctionitem
    })


# view for a specific item which was clicked on
def listings(request, product_id):
        requested_item = AuctionItems.objects.get(id = product_id)

        if request.method == "POST":
            comment = CommentForm(request.POST)
            if comment.is_valid():
                on_comment(request, comment.cleaned_data['comment'], requested_item)

        comment_box = CommentForm()
        all_comments = Comments.objects.filter(product = requested_item)
        
        #to access the watchlist user must be logged in
        if request.user.is_authenticated:
            currently_loggedin = User.objects.get(username=request.user.username)
            watching_items = WatchList.objects.get(account_owner=currently_loggedin).products.all()
            if requested_item in watching_items:
                watchlist_status = "remove from watchlist"
            else:
                watchlist_status = "add to watchlist"
        else:
            watchlist_status = "Null"
        return render(request, "auctions/item.html", {
            "item" : requested_item,
            "comment_box" : comment_box,
            "all_comments" : all_comments,
            "watchlist_btn" : watchlist_status
        })


@login_required
def on_comment(request, content, product):
    author = User.objects.get(username = request.user.username)
    comment = Comments(comment=content, author=author, product=product)
    comment.save()


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

@login_required
def update_watchlist(request, product_id):
    currently_loggedin = User.objects.get(username=request.user.username)
    target_product = AuctionItems.objects.get(id=product_id)
    
    #this is to check whether there a object exists according to the username
    try:
        watching_items_names = WatchList.objects.get(account_owner=currently_loggedin) #filtering the account to get the products
    except WatchList.DoesNotExist:
        watchlist_obj = WatchList.objects.create(account_owner=currently_loggedin)
        watchlist_obj.products.add(target_product)
        watchlist_obj.save()
        return redirect('listings', product_id)
    
    # checking if the requested product exists in the watchlist
    required_item = watching_items_names.products.all()
    if target_product in required_item:
        watching_items_names.products.remove(target_product)
        watching_items_names.save()
        return redirect('listings', product_id)
    else:
        watching_items_names.products.add(target_product)
        watching_items_names.save()
        return redirect('listings', product_id)


@login_required
def watchlist(request):
    currently_loggedin = User.objects.get(username=request.user.username)
    #this is to check whether there a object exists according to the username
    try:
        watching_items_names = WatchList.objects.get(account_owner=currently_loggedin) #filtering the account to get the products
    except WatchList.DoesNotExist:
       return render(request, "auctions/watchlist.html", {
        "all_auctionitems" : None
    })

    watching_items = watching_items_names.products.all() #getting the products
    return render(request, "auctions/watchlist.html", {
        "all_auctionitems" : watching_items
    })
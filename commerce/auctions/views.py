from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionItems, Comments
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
def listings(request, id):
        requested_item = AuctionItems.objects.get(id = id)

        if request.method == "POST":
            comment = CommentForm(request.POST)
            if comment.is_valid():
                on_comment(request, comment.cleaned_data['comment'], requested_item)

        comment_box = CommentForm()
        all_comments = Comments.objects.filter(product = requested_item)
        return render(request, "auctions/item.html", {
            "item" : requested_item,
            "comment_box" : comment_box,
            "all_comments" : all_comments
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
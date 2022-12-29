from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bids, Comments, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "all_listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return index(request)
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return index(request)


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
        return index(request)
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        print(request.POST)
        name = request.POST["item_name"]
        url = request.POST["image_url"]
        cat = request.POST["category"]
        desc = request.POST["description"]
        price = request.POST["price"]
        current_user = request.user

        new_listing = Listing(item_name=name, 
        image_url=url, 
        category=cat, 
        description=desc, 
        current_bid=price, 
        created_by=current_user,
        completed=False)
        new_listing.save()

        return index(request)
    else:
        return render(request, "auctions/create_listing.html")

def listing(request, listing_id):
    item = Listing.objects.filter(id=listing_id).first()
    gray_out = (request.user == item.created_by)
    print(f'USER: {gray_out}')
    return render(request, "auctions/listing.html", {
        "listing" : item,
        "gray_out" : gray_out
    })
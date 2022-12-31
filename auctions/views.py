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
    current_user = request.user
    first_bid = Bids.objects.filter(item_bidding=item).first() == None
    completed = item.completed

    if first_bid:
        current_price = item.current_bid
    else:
        current_price = item.current_bid + 0.01

    if request.method == "POST":
        # Check if buttons add or remove from the watchlist.
        if request.POST.get("watchlist_add"):
            new_watchlist = Watchlist(
                watchlist_user=current_user,
                watchlist_item=item
            )
            new_watchlist.save()
        elif request.POST.get("watchlist_remove"):
            removing_watchlist = Watchlist.objects.filter(
                watchlist_user=current_user,
                watchlist_item=item
            ).first()
            removing_watchlist.delete()
        elif request.POST.get("bid_new"):
            new_price = request.POST.get("bid_price")
            current_price = new_price
            if len(Bids.objects.filter(item_bidding=item)) >= 1:
                bid_to_update = Bids.objects.get(item_bidding=item)
                bid_to_update.bidding_offer = new_price
                bid_to_update.save()
                item.current_bid = new_price
                item.save()
                print("Entry has a bid placed")
            else:
                new_bid = Bids(bidder=current_user, bidding_offer=new_price, item_bidding=item)
                new_bid.save()
                print("Entry has no bid placed")
        elif request.POST.get("bid_end"):
            item.completed = True
            item.save()
            

        #Check if button adds more to the bid.
    add_or_remove = len(Watchlist.objects.filter(watchlist_user=current_user, watchlist_item=item))
    return render(request, "auctions/listing.html", {
        "listing" : item,
        "gray_out" : gray_out,
        "add_or_remove" : add_or_remove,
        "min_price" : current_price,
        "first_bid" : first_bid,
        "completed" : completed
    })
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    item_name = models.CharField(max_length=96)
    image_url = models.URLField()
    category = models.CharField(max_length=64)
    description = models.TextField()
    completed = models.BooleanField()
    current_bid = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller", default=User.objects.filter(id=1).first())

class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bidding_offer = models.FloatField()
    item_bidding = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_bidding")

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    item_to_comment = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_to_comment")
    comment = models.TextField()

class Watchlist(models.Model):
    watchlist_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    watchlist_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_item")
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
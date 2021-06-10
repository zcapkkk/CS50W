from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(name="Product Name", max_length=120)
    seller = models.ForeignKey(User, on_delete=CASCADE, name="Seller")
    description = models.TextField(name="Product Description")
  

class Bid(models.Model):
    price = models.DecimalField(name="Bidding Price", max_digits=20, decimal_places=2)
    product = models.ForeignKey(Listing, on_delete=CASCADE)

class Comment(models.Model):
    product = models.ForeignKey(Listing, on_delete=CASCADE)
    poster = models.ForeignKey(User, on_delete=CASCADE)
    text = models.TextField(name="User Comment")

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    startingbid = models.DecimalField(max_digits=16, decimal_places=2)
    imageurl = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    
    def __str__(self):
        return f"{self.title}: object {self.id}"
    

class Bid(models.Model):
    user = models.ForeignKey(User, related_name="bidder", on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, related_name="bidobject", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=16, decimal_places=2)

    def __str__(self):
        return f"{self.price} on {self.item} by {self.user}"

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="commenter", on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, related_name="commentobject", on_delete=models.CASCADE)
    text = models.TextField()


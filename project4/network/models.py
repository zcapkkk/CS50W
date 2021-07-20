from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster} on {self.date}"


class Like(models.Model):
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liker = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="likes", null=True)
    date = models.DateTimeField(auto_now_add=True)

        
    class Meta:
        unique_together = [["liker", "parent_post"]]

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fan")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="influencer")

    class Meta:
        unique_together = [["follower", "following"]]

    def __str__(self):
        return f"{self.follower} is following {self.following}"



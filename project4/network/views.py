from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.base import Model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like, Follow



def index(request):
    if request.method == "POST":
        post = Post(
            poster = request.user,
            post = request.POST["post"],
        )
        post.save()

        return HttpResponseRedirect(reverse("index"))


    return render(request, "network/index.html", {
        "posts": Post.objects.order_by('-date')
    })

def profile(request, username):

    if request.method == 'POST':
        # do something that prevents repeat
        followlink = Follow(
            follower = request.user,
            following = User.objects.get(username=follow_this_user)
        )
        followlink.save()
        

    # verify user_id exists

    userprofile = User.objects.get(username=username)

    return render(request, "network/profile.html", {
        "userprofile": userprofile,
        "user_posts": Post.objects.filter(poster=userprofile),
        "follows": Follow.objects.filter(follower=request.user)
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

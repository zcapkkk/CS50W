import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.base import Model
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

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

    try:
        User.objects.get(username=username)
    except ObjectDoesNotExist: 
        return HttpResponse("User does not exist")

    userprofile = User.objects.get(username=username)
    followinglist = Follow.objects.filter(follower=request.user).values_list('following', flat=True)

    if request.method == 'POST':
        # do something that prevents repeat

       
        followthis = str(request.POST["followthis"])
        followthis = User.objects.get(username=followthis)
        followthisid = followthis.id

        if followthisid not in followinglist:
            followlink = Follow(
                follower = request.user,
                following = followthis
            )
            followlink.save()
        else:
            Follow.objects.get(follower=request.user,following=followthis).delete()

        return HttpResponseRedirect(reverse("profile", args=(request.user.username,)))

        
    # verify user_id exists

    if request.user.is_authenticated:
        return render(request, "network/profile.html", {
            "userprofile": userprofile,
            "user_posts": Post.objects.filter(poster=userprofile),
            "follows": Follow.objects.filter(follower=request.user),
            "followinglist": followinglist
        })
    else:
        return render(request, "network/profile.html", {
            "userprofile": userprofile,
            "user_posts": Post.objects.filter(poster=userprofile),
            "follows": None
        })

def following(request):
    user = request.user
    follows = Follow.objects.filter(follower=user).values_list("following")
    followinglist = [follow[0] for follow in follows]

    posts = Post.objects.filter(poster__in=followinglist).order_by('-date')


    return render(request, "network/following.html", {
        "posts": posts
    })

def like(request, id):
    pass


@login_required 
def edit(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        data = json.loads(request.body)
        post.post = data.get("text","")
        post.save()
        
    return JsonResponse({"postUpdate": post.post})

    
@login_required
def like(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        action = str(data.get("action",""))
        if action == "like":
            # do some error checking,
            # like if cannot get object id or cannot get request.user

            likeobject = Like(parent_post = Post.objects.get(id=id), liker=request.user)
            likeobject.save()
            return JsonResponse({"message": "liked"})
        
        if action == "unlike":

            likeobject= Like.objects.get(parent_post = Post.objects.get(id=id), liker=request.user)
            likeobject.delete()
            return JsonResponse({"message": "unliked"})
        else:
            return HttpResponse("Bad command")

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



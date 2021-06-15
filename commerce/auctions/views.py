from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment, Watchitem

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]

class CreateForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "startingbid", "imageurl", "category"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]



def index(request):
    return render(request, "auctions/index.html", {
        "Listing": Listing.objects.all()
        })

def listing(request, item_id):
    bids = Bid.objects.filter(item_id=item_id).order_by('-price').values()
    if bids.exists():
        topbid = bids[0]
        topbid = topbid['price'] 
    else:
        bids = "No bids"
        topbid = "No bids"
        
    return render(request, "auctions/listing.html", {
        "item": Listing.objects.get(id=item_id),
        "bids": bids,
        "topbid":topbid,
        "comments": Comment.objects.filter(item_id=item_id)
        })

@login_required
def bid(request, item_id):

    startingprice = Listing.objects.get(id=item_id).startingbid

    # get current highest bid
    bids = Bid.objects.filter(item_id=item_id).order_by('-price').values()
    if bids.exists():
        bids = bids[0]
        currentTopbid = bids['price']
    else:
        currentTopbid = startingprice

    if request.method=="POST":
        bidform = BidForm(request.POST)


        # check if bid is higher than the top bid
        if float(request.POST["price"]) <= currentTopbid:
            return render(request, "auctions/bid.html", {
                "form": bidform,
                "item": Listing.objects.get(id=item_id),
                "message": "Please place a bid higher than the current bid",
                "topbid": currentTopbid,
                "startingprice": startingprice
            })
        else:
            newbidform = bidform.save(commit=False)
            newbidform.user = request.user
            newbidform.item = Listing.objects.get(id=item_id)
            newbidform.save()

            return HttpResponseRedirect(reverse("listing", args=(item_id,)))
   

    return render(request, "auctions/bid.html", {
        "form": BidForm(),
        "item": Listing.objects.get(id=item_id),
        "topbid": currentTopbid,
        "startingprice": startingprice
        })


@login_required
def create(request):
    if request.method=="POST":
        form = CreateForm(request.POST)
        newbid = form.save(commit=False)
        newbid.seller = request.user
        newbid.save()
        return HttpResponseRedirect(reverse(index))

    else:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse(index))
    
    return render(request, "auctions/create.html", {"form": CreateForm()})
    

@login_required
def comment(request, item_id):
    if request.method == "POST":
        commentform = CommentForm(request.POST)

        newcommentform = commentform.save(commit=False)
        newcommentform.user=request.user
        newcommentform.item = Listing.objects.get(id=item_id)

        newcommentform.save()

        return HttpResponseRedirect(reverse("listing", args=(item_id,)))


    return render(request, "auctions/comment.html", {"form": CommentForm(), "item": Listing.objects.get(id=item_id)})


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

@login_required
def watchlist(request, user_id):
    if request.method=="POST":
        if Watchitem.objects.filter(item_id=request.POST["item_id"]).exists():
            return render(request, "auctions/watchlist.html", {"watchlist":Watchitem.objects.filter(user_id=user_id)})
        witem = Watchitem(user=request.user, item = Listing.objects.get(id=request.POST["item_id"]))
        witem.save()

    if request.method=="GET":
        if User.objects.get(id=user_id) != request.user:
            return HttpResponse("Denied access")


    return render(request, "auctions/watchlist.html", {"watchlist":Watchitem.objects.filter(user_id=user_id)})
    
        
        

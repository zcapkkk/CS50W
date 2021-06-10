from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.widgets import Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import Listing

from .models import User

# class CreateForm(forms.Form):
#     name = forms.CharField(max_length=120, label="Product Name")
#     description = forms.CharField(label="Product Description", widget=Textarea)
#     price = forms.DecimalField(label="Starting Price", decimal_places=2, max_digits=20)

class CreateForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields =  ['Product Name','Product Description','Seller']



def index(request):
    return render(request, "auctions/index.html")


def create(request):
    if request.method == "POST":
        listingForm = CreateForm(request.POST)
        if listingForm.is_valid(): 
            listingForm.save()
            return HttpResponseRedirect(reverse('auctions:index'))
        else:
            return render(request, "auctions/create.html", {"form":  listingForm})          

    return render(request, "auctions/create.html", {"form": CreateForm()})

    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

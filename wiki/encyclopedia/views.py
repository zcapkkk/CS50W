from typing import Text
from django.forms.widgets import Textarea
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from random import choice
from django.urls import reverse
from django.utils.html import word_split_re
from django import forms

import markdown2
from . import util

class NewPage(forms.Form):
    title = forms.CharField(max_length=120, label="Entry Name")
    body = forms.CharField(widget=Textarea, label="Entry")



def edit(request, entryName):

    if request.method == "POST":
        form = NewPage(request.POST)

        if form.is_valid():
            newentry = form.cleaned_data["body"]
            util.save_entry(entryName, newentry)

            return HttpResponseRedirect(reverse('entry', kwargs={'entryName':entryName}))
            
        else:
            return render(request, "encyclopedia/edit.html", {"form": form, "entryName": entryName})



    markdown = util.get_entry(entryName)
    return render(request, "encyclopedia/edit.html",{
        "form": NewPage(initial={
            'title': entryName,
            'body': markdown
        }),
        "entryName": entryName})


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entryName):
    if entryName not in util.list_entries():
        return HttpResponseNotFound("Page does not exists.")
    else:
        html = markdown2.markdown(util.get_entry(entryName))
    
    return render(request, "encyclopedia/entry.html", {
        "entry" : html,
        "entryName": entryName
    })


def search(request):
    if request.method == "GET":
        item = request.GET
        query = item["q"]
        if query in util.list_entries():
            return HttpResponseRedirect(reverse('entry', args=[query]))
        else:
            results = []
            for word in util.list_entries():
                if query.lower() in word.lower():
                    results.append(word)
            
            return render(request, "encyclopedia/search.html", {'results': results})


 
def create(request):
    # check method
    if request.method == 'POST':
        
        form = NewPage(request.POST)

        # check validity
        if form.is_valid():
            # break down the form
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]

            util.save_entry(title, body)

            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "encyclopedia/create.html", {"form": form})

    return render(request, "encyclopedia/create.html", {"form": NewPage()})







def random(request):
    return entry(request, choice(util.list_entries()))


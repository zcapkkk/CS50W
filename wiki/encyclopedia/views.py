from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from random import choice
from django.urls import reverse
from django.utils.html import word_split_re

import markdown2
from . import util



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
        "entry" : html
    })


def search(request):
    if request.method == "GET":
        item = request.GET
        query = item["q"]
        if query in util.list_entries():
            return HttpResponseRedirect(f"wiki/{query}")
        else:
            results = []
            for word in util.list_entries():
                if query.lower() in word.lower():
                    results.append(word)
            
            return render(request, "encyclopedia/search.html", {'results': results})







 
def create(request):
    return render(request, "encyclopedia/create.html")

def random(request):
    return entry(request, choice(util.list_entries()))


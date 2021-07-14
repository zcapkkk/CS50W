from django.http.response import Http404, HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "multipage/index.html")

texts = ["Text 1", "Text 2", "Text 3"]

def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num - 1])
    else:
        return Http404("Page does not exist")


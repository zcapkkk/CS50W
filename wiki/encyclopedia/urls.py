from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryName>", views.entry, name="entry"),
    path("create", views.create, name="create"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search")
]

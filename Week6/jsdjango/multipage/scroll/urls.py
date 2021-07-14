from . import views
from django.urls import path

urlpatterns = [

    path("", views.index, "index"),
    path("posts", views.posts, "posts"),
]
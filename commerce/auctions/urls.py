from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:item_id>", views.listing, name="listing"),
    path("listing/<int:item_id>/bid", views.bid, name="bid"),
    path("listing/<int:item_id>/comment", views.comment, name="comment"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist")
]

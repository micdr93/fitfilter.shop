from django.urls import path
from . import views

urlpatterns = [
    path("activities/", views.user_activity_list, name="user_activity_list"),
    path("wishlist/", views.wishlist_view, name="wishlist_view"),
    path("preferences/", views.user_preferences_view, name="user_preferences"),
]

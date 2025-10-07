from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
]
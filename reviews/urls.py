from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('write/<int:product_id>/', views.write_review, name='write_review'),
    path('product/<int:product_id>/', views.product_reviews, name='product_reviews'),
    path('helpful/<int:review_id>/', views.review_helpful, name='review_helpful'),
]
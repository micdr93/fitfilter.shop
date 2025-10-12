from django.urls import path
from . import views

app_name = 'affiliates'

urlpatterns = [
    path('redirect/<int:link_id>/', views.affiliate_redirect, name='affiliate_redirect'),
]
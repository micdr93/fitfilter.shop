from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Style preferences
    preferred_colors = models.JSONField(default=list)  # ["black", "white", "blue"]
    preferred_brands = models.ManyToManyField('products.Brand', blank=True)
    preferred_categories = models.ManyToManyField('products.Category', blank=True)
    
    # Price preferences
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Fit preferences
    preferred_fit_types = models.JSONField(default=list)  # ["slim", "regular"]
    
    updated_at = models.DateTimeField(auto_now=True)

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    
    ACTIVITY_TYPES = [
        ('view', 'Viewed'),
        ('like', 'Liked'),
        ('click', 'Clicked Affiliate Link'),
        ('purchase', 'Purchased'),
        ('review', 'Reviewed'),
    ]
    
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Additional context
    session_id = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=50, blank=True)  # "search", "recommendation", etc.

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    
    # Size preferences for this item
    preferred_size = models.CharField(max_length=20, blank=True)
    preferred_color = models.CharField(max_length=50, blank=True)
    
    # Notifications
    notify_price_drop = models.BooleanField(default=True)
    notify_back_in_stock = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'product']

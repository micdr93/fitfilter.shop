import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AffiliatePartner(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    website = models.URLField()
    api_endpoint = models.URLField(blank=True)
    api_key = models.CharField(max_length=200, blank=True)
    
    # Commission settings
    default_commission_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.05)
    cookie_duration_days = models.IntegerField(default=30)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class AffiliateLink(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    partner = models.ForeignKey(AffiliatePartner, on_delete=models.CASCADE)
    
    # Link details
    affiliate_url = models.URLField()
    deep_link = models.URLField(blank=True)  # Direct to product page
    
    # Tracking
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    
    # Pricing at partner
    partner_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    last_checked = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['product', 'partner']


class ClickTracking(models.Model):
    affiliate_link = models.ForeignKey(AffiliateLink, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Tracking details
    session_id = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.URLField(blank=True)
    
    # Conversion tracking
    tracking_id = models.UUIDField(default=uuid.uuid4, unique=True)
    converted = models.BooleanField(default=False)
    conversion_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    commission_earned = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    clicked_at = models.DateTimeField(auto_now_add=True)
    converted_at = models.DateTimeField(null=True, blank=True)


# 🔥 Added models to fix ImportError
class Review(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField()  # 1–5 stars
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}★"


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="review_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.review}"

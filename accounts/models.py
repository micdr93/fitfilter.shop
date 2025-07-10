from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say')
    ], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

class SizeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Clothing sizes
    shirt_size = models.CharField(max_length=10, choices=[
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ], blank=True)
    
    pant_size = models.CharField(max_length=10, blank=True)  # e.g., "32x34"
    dress_size = models.CharField(max_length=10, blank=True)
    
    # Shoe sizes
    shoe_size_us = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    shoe_size_eu = models.IntegerField(null=True, blank=True)
    shoe_size_uk = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    
    # Body measurements (optional for better fit)
    height_cm = models.IntegerField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    chest_cm = models.IntegerField(null=True, blank=True)
    waist_cm = models.IntegerField(null=True, blank=True)
    hip_cm = models.IntegerField(null=True, blank=True)
    
    # Preferences
    preferred_fit = models.CharField(max_length=20, choices=[
        ('slim', 'Slim Fit'),
        ('regular', 'Regular Fit'),
        ('loose', 'Loose Fit'),
        ('oversized', 'Oversized'),
    ], default='regular')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# products/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    website = models.URLField(blank=True)
    size_guide_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    # Original product details
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Product images
    main_image = models.ImageField(upload_to='products/')
    
    # Product attributes
    material = models.CharField(max_length=200, blank=True)
    care_instructions = models.TextField(blank=True)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.brand.name} - {self.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    color_code = models.CharField(max_length=7, blank=True)  # hex color
    size = models.CharField(max_length=20)
    size_type = models.CharField(max_length=20, choices=[
        ('clothing', 'Clothing'),
        ('shoe', 'Shoe'),
        ('accessory', 'Accessory'),
    ])
    
    # Stock and availability
    stock_quantity = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    
    # Pricing (if variant has different pricing)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'color', 'size']
    
    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size}"

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count, Min, Max
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category, Brand, ProductVariant
from accounts.models import SizeProfile
from recommendations.models import UserActivity, Wishlist
from reviews.models import Review
import json

def home(request):
    """Homepage with personalized recommendations"""
    # Featured products
    featured_products = Product.objects.filter(
        is_active=True,
        variants__is_available=True
    ).distinct()[:8]
    
    # Get user's size profile for personalized recommendations
    size_matched_products = []
    if request.user.is_authenticated:
        try:
            size_profile = request.user.sizeprofile
            # Find products that match user's sizes
            size_matched_products = Product.objects.filter(
                variants__size__in=[
                    size_profile.shirt_size,
                    size_profile.pant_size,
                    str(size_profile.shoe_size_us)
                ],
                is_active=True,
                variants__is_available=True
            ).distinct()[:6]
        except SizeProfile.DoesNotExist:
            pass
    
    # Popular categories
    popular_categories = Category.objects.filter(
        product__is_active=True
    ).annotate(
        product_count=Count('product')
    ).order_by('-product_count')[:6]
    
    return render(request, 'products/home.html', {
        'featured_products': featured_products,
        'size_matched_products': size_matched_products,
        'popular_categories': popular_categories,
    })

def product_list(request):
    """Product listing with filtering and search"""
    products = Product.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__name__icontains=search_query)
        )
    
    # Category filtering
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Brand filtering
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
    
    # Size filtering (if user is logged in)
    if request.user.is_authenticated:
        try:
            size_profile = request.user.sizeprofile
            size_filter = request.GET.get('size_filter')
            if size_filter == 'my_sizes':
                user_sizes = [
                    size_profile.shirt_size,
                    size_profile.pant_size,
                    str(size_profile.shoe_size_us)
                ]
                products = products.filter(
                    variants__size__in=user_sizes,
                    variants__is_available=True
                ).distinct()
        except SizeProfile.DoesNotExist:
            pass
    
    # Price filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(current_price__gte=min_price)
    if max_price:
        products = products.filter(current_price__lte=max_price)
    
    # Availability filtering
    availability = request.GET.get('availability')
    if availability == 'in_stock':
        products = products.filter(variants__stock_quantity__gt=0)
    
    # Sorting
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('current_price')
    elif sort_by == 'price_high':
        products = products.order_by('-current_price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'rating':
        products = products.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating')
    else:
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Filter options for sidebar
    categories = Category.objects.filter(product__is_active=True).distinct()
    brands = Brand.objects.filter(product__is_active=True).distinct()
    
    # Price range for filter
    price_range = Product.objects.filter(is_active=True).aggregate(
        min_price=Min('current_price'),
        max_price=Max('current_price')
    )
    
    context = {
        'products': page_obj,
        'categories': categories,
        'brands': brands,
        'price_range': price_range,
        'search_query': search_query,
        'current_category': category_slug,
        'current_brand': brand_slug,
        'current_sort': sort_by,
    }
    
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    """Product detail page with size availability"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Track user activity
    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user,
            product=product,
            activity_type='view',
            session_id=request.session.session_key or 'anonymous'
        )
    
    # Get available variants
    variants = product.variants.filter(is_available=True)
    
    # Get user's size profile for highlighting matching sizes
    user_sizes = []
    if request.user.is_authenticated:
        try:
            size_profile = request.user.sizeprofile
            user_sizes = [
                size_profile.shirt_size,
                size_profile.pant_size,
                str(size_profile.shoe_size_us)
            ]
        except SizeProfile.DoesNotExist:
            pass
    
    # Get reviews and ratings
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    rating_counts = {}
    for i in range(1, 6):
        rating_counts[i] = reviews.filter(rating=i).count()
    
    # Get affiliate links
    affiliate_links = product.affiliatelink_set.filter(
        is_active=True,
        partner__is_active=True
    ).order_by('partner_price')
    
    # Check if user has wishlisted this product
    is_wishlisted = False
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).exists()
    
    # Similar products
    similar_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:6]
    
    context = {
        'product': product,
        'variants': variants,
        'user_sizes': user_sizes,
        'reviews': reviews[:5],  # Show first 5 reviews
        'avg_rating': avg_rating,
        'rating_counts': rating_counts,
        'affiliate_links': affiliate_links,
        'is_wishlisted': is_wishlisted,
        'similar_products': similar_products,
    }
    
    return render(request, 'products/product_detail.html', context)

@login_required
def toggle_wishlist(request, product_id):
    """Add/remove product from wishlist"""
    product = get_object_or_404(Product, id=product_id)
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if not created:
        wishlist_item.delete()
        action = 'removed'
    else:
        action = 'added'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'action': action,
            'wishlisted': created
        })
    
    return redirect('products:product_detail', slug=product.slug)

def size_availability(request, product_id):
    """AJAX endpoint for size availability"""
    product = get_object_or_404(Product, id=product_id)
    color = request.GET.get('color')
    
    variants = product.variants.filter(is_available=True)
    if color:
        variants = variants.filter(color=color)
    
    sizes = []
    for variant in variants:
        sizes.append({
            'size': variant.size,
            'stock': variant.stock_quantity,
            'available': variant.stock_quantity > 0
        })
    
    return JsonResponse({'sizes': sizes})
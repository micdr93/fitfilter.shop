from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import UserActivity, Wishlist, UserPreference
from products.models import Product
from accounts.models import SizeProfile

@login_required
def wishlist_view(request):
    """User's wishlist"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product').order_by('-created_at')
    
    return render(request, 'recommendations/wishlist.html', {
        'wishlist_items': wishlist_items
    })

@login_required
def recommendations_view(request):
    """Personalized product recommendations"""
    user = request.user
    
    # Get user's activity history
    viewed_products = UserActivity.objects.filter(
        user=user,
        activity_type='view'
    ).values_list('product_id', flat=True)
    
    # Get user's size profile
    try:
        size_profile = user.sizeprofile
    except SizeProfile.DoesNotExist:
        size_profile = None
    
    # Recommendation 1: Based on viewed categories
    recommended_by_category = []
    if viewed_products:
        viewed_categories = Product.objects.filter(
            id__in=viewed_products
        ).values_list('category', flat=True).distinct()
        
        recommended_by_category = Product.objects.filter(
            category__in=viewed_categories,
            is_active=True
        ).exclude(id__in=viewed_products)[:8]
    
    # Recommendation 2: Size-matched products
    size_matched = []
    if size_profile:
        user_sizes = [
            size_profile.shirt_size,
            size_profile.pant_size,
            str(size_profile.shoe_size_us)
        ]
        size_matched = Product.objects.filter(
            variants__size__in=user_sizes,
            variants__is_available=True,
            is_active=True
        ).distinct().exclude(id__in=viewed_products)[:8]
    
    # Recommendation 3: Popular products
    popular_products = Product.objects.filter(is_active=True).annotate(
        view_count=Count('useractivity', filter=Q(useractivity__activity_type='view'))
    ).order_by('-view_count')[:8]
    
    context = {
        'recommended_by_category': recommended_by_category,
        'size_matched': size_matched,
        'popular_products': popular_products,
    }
    
    return render(request, 'recommendations/recommendations.html', context)
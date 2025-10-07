# affiliates/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AffiliatePartner, AffiliateLink, ClickTracking
from recommendations.models import UserActivity  # ✅ Import it

def affiliate_redirect(request, link_id):
    """Track affiliate link clicks and redirect"""
    affiliate_link = get_object_or_404(AffiliateLink, id=link_id, is_active=True)
    
    # Track the click
    click_tracking = ClickTracking.objects.create(
        affiliate_link=affiliate_link,
        user=request.user if request.user.is_authenticated else None,
        session_id=request.session.session_key or 'anonymous',
        ip_address=request.META.get('REMOTE_ADDR', ''),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        referrer=request.META.get('HTTP_REFERER', '')
    )
    
    # Update click count
    affiliate_link.clicks += 1
    affiliate_link.save()
    
    # Track user activity
    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user,
            product=affiliate_link.product,
            activity_type='click',
            session_id=request.session.session_key or 'anonymous'
        )
    
    # Set tracking cookie
    response = redirect(affiliate_link.affiliate_url)
    response.set_cookie(
        'ff_tracking',
        str(click_tracking.tracking_id),
        max_age=60*60*24*affiliate_link.partner.cookie_duration_days
    )
    
    return response

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Review, ReviewImage
from products.models import Product

@login_required
def write_review(request, product_id):
    """Write a review for a product"""
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user already reviewed this product
    existing_review = Review.objects.filter(
        user=request.user,
        product=product
    ).first()
    
    if existing_review:
        messages.warning(request, 'You have already reviewed this product.')
        return redirect('products:product_detail', slug=product.slug)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        content = request.POST.get('content')
        size_purchased = request.POST.get('size_purchased')
        fit_rating = request.POST.get('fit_rating')
        
        review = Review.objects.create(
            user=request.user,
            product=product,
            rating=rating,
            title=title,
            content=content,
            size_purchased=size_purchased,
            fit_rating=fit_rating
        )
        
        # Handle review images
        images = request.FILES.getlist('images')
        for image in images:
            ReviewImage.objects.create(
                review=review,
                image=image
            )
        
        messages.success(request, 'Review submitted successfully!')
        return redirect('products:product_detail', slug=product.slug)
    
    return render(request, 'reviews/write_review.html', {
        'product': product
    })

def product_reviews(request, product_id):
    """View all reviews for a product"""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'reviews/product_reviews.html', {
        'product': product,
        'reviews': page_obj
    })

@login_required
def review_helpful(request, review_id):
    """Mark review as helpful"""
    review = get_object_or_404(Review, id=review_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'helpful':
            review.helpful_votes += 1
        elif action == 'unhelpful':
            review.unhelpful_votes += 1
        review.save()
    
    return JsonResponse({
        'helpful_votes': review.helpful_votes,
        'unhelpful_votes': review.unhelpful_votes
    })
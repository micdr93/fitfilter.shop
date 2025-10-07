from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
        help_text='You can upload multiple images (optional)'
    )
    
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content', 'size_purchased', 'fit_rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'fit_rating': forms.RadioSelect(choices=[
                (1, 'Very Small'),
                (2, 'Small'),
                (3, 'True to Size'),
                (4, 'Large'),
                (5, 'Very Large')
            ]),
            'content': forms.Textarea(attrs={'rows': 4}),
        }

print("Core views, URLs, and forms created!")
print("This includes:")
print("- User registration and profile management")
print("- Product listing with filtering and search")
print("- Size-based recommendations")
print("- Affiliate link tracking")
print("- Review system with fit ratings")
print("- Wishlist functionality")
print("- Personalized recommendations")
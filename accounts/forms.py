from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, SizeProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class SizeProfileForm(forms.ModelForm):
    class Meta:
        model = SizeProfile
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'height_cm': forms.NumberInput(attrs={'placeholder': 'Height in cm'}),
            'weight_kg': forms.NumberInput(attrs={'placeholder': 'Weight in kg'}),
            'chest_cm': forms.NumberInput(attrs={'placeholder': 'Chest measurement in cm'}),
            'waist_cm': forms.NumberInput(attrs={'placeholder': 'Waist measurement in cm'}),
            'hip_cm': forms.NumberInput(attrs={'placeholder': 'Hip measurement in cm'}),
        }
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import User, SizeProfile
from .forms import UserRegistrationForm, SizeProfileForm

class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:profile_setup')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        messages.success(self.request, 'Account created successfully!')
        return response

@login_required
def profile_setup(request):
    """Setup size profile after registration"""
    size_profile, created = SizeProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = SizeProfileForm(request.POST, instance=size_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Size profile updated successfully!')
            return redirect('products:home')
    else:
        form = SizeProfileForm(instance=size_profile)
    
    return render(request, 'accounts/profile_setup.html', {'form': form})

@login_required
def profile_view(request):
    """View and edit user profile"""
    size_profile, created = SizeProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = SizeProfileForm(request.POST, instance=size_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
    else:
        form = SizeProfileForm(instance=size_profile)
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'size_profile': size_profile
    })
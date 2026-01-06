# home/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # <--- Moved here to fix your error

# Import models and forms
from .models import BlogModel, Profile
from .forms import BlogForm, RegisterForm, UpdateUserForm, UpdateProfileForm

# 1. Home View
def home(request):
    try:
        posts = BlogModel.objects.all().order_by('-created_at')
    except Exception:
        posts = []
    context = {'posts': posts}
    return render(request, 'blog.html', context)

# 2. Authentication Views
def login_view(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        messages.error(request, "Registration failed. Please check the information.")
    else:
        form = RegisterForm()
        
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# 3. Blog Logic Views
@login_required
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog_obj = form.save(commit=False)
            blog_obj.user = request.user
            blog_obj.save()
            return redirect('home')
    else:
        form = BlogForm()
    return render(request, 'add_blogs.html', {'form': form})

def blog_detail(request, slug):
    post = get_object_or_404(BlogModel, slug=slug)
    return render(request, 'blog_detail.html', {'post': post})

@login_required
def delete_blog_post(request, slug):
    post = get_object_or_404(BlogModel, slug=slug)
    if post.user == request.user:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    return redirect('profile')

@login_required
def edit_blog_post(request, slug):
    post = get_object_or_404(BlogModel, slug=slug)
    
    # Security check: only owner can edit
    if post.user != request.user:
        return redirect('home')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', slug=post.slug)
    else:
        form = BlogForm(instance=post)
    return render(request, 'add_blogs.html', {'form': form})

# 4. Profile & Search
@login_required
def profile(request):
    # Show only the logged-in user's posts
    user_posts = BlogModel.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'posts': user_posts})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST, instance=request.user)
        # Try to get existing profile, or create one if missing
        profile, created = Profile.objects.get_or_create(user=request.user)
        p_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UpdateUserForm(instance=request.user)
        profile, created = Profile.objects.get_or_create(user=request.user)
        p_form = UpdateProfileForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'edit_profile.html', context)

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        # Case-insensitive search on title
        results = BlogModel.objects.filter(title__icontains=query)
    return render(request, 'search.html', {'results': results})
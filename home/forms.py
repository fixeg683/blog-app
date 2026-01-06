from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import BlogModel, Profile

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel  # <--- Updated to match your actual model name
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your story...'}),
        }

class RegisterForm(UserCreationForm):
    # Adds email to the standard registration form
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_verified'] # Add other profile fields if you have them, e.g. avatar
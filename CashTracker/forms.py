from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Staff

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Staff
        fields = ('username', 'email', 'role', 'password1', 'password2')
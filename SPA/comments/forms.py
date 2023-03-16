from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField
from django import forms

from .models import *


class AddCommentForm(forms.ModelForm):
    image = forms.ImageField(label='Image', required=False,
                             widget=forms.ClearableFileInput(attrs={'multiple': False, 'accept': '.jpg, .png, .gif'}))
    file = forms.FileField(label='File', required=False,
                           widget=forms.ClearableFileInput(attrs={'multiple': False, 'accept': '.txt'}))

    class Meta:
        model = Comment
        fields = ('body', 'image', 'file', 'parent')
        widgets = {
            'parent': forms.HiddenInput()
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Password again', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'password')

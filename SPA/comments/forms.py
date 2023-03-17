from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django import forms
import re

from django.core.exceptions import ValidationError

from .models import Comment, Profile


def reg_validator(text):
    tag_regex = re.compile(
        r"<(?P<tag>(a|i|strong|code))\s*(?P<href>\s+href=(?P<q_mark>\"|\')[^\"<>]*(?P=q_mark))?(?P<title>\s+title=(?P<q_mark2>\"|\')[^\"<>]*(?P=q_mark2))?>[^<>]*</(?P=tag)>")
    re_all = re.findall(tag_regex, text)
    while re_all:
        for re_obj in re_all:
            if (re.search(r'href|title', re_obj[4]) or re.search(r'href|title', re_obj[4])) and re_obj[0] != 'a':
                raise ValidationError('tags are wrong')
        text = re.sub(tag_regex, '', text)
        re_all = re.findall(tag_regex, text)

    if '<' in text or '>' in text:
        raise ValidationError('tags are wrong')


class AddCommentForm(forms.ModelForm):
    image = forms.ImageField(label='Image', required=False,
                             widget=forms.ClearableFileInput(attrs={'multiple': False, 'accept': '.jpg, .png, .gif'}))
    file = forms.FileField(label='File', required=False,
                           widget=forms.ClearableFileInput(attrs={'multiple': False, 'accept': '.txt'}))

    def clean_body(self):
        body = self.cleaned_data['body']
        reg_validator(body)
        return body

    class Meta:
        model = Comment
        fields = ('body', 'image', 'file', 'parent')
        widgets = {
            'parent': forms.HiddenInput(attrs={'class': 'hidden-input-parent'})
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

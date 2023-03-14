from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView

from .models import *
from .forms import *


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'comments/register.html'
    success_url = reverse_lazy('main')


class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'comments/login.html'

    def get_success_url(self):
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    return redirect('main')


class CommentListView(ListView):
    model = Comment
    template_name = 'comments/index.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(parent=None).prefetch_related('replies__replies')

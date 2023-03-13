from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView

from .models import *


class CommentListView(ListView):
    model = Comment
    template_name = 'comments/index.html'

    def get_queryset(self):
        return Comment.objects.all()

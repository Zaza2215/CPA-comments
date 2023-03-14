from django.shortcuts import render
from django.views.generic import ListView

from .models import *


class CommentListView(ListView):
    model = Comment
    template_name = 'comments/index.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(parent=None).prefetch_related('replies__replies')

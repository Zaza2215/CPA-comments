from django.urls import path

from .views import *

urlpatterns = [
    # path("login/", LoginUser.as_view(), name="login"),
    path("", CommentListView.as_view(), name='main'),
    path('register/', RegisterUser.as_view(), name='register'),
]

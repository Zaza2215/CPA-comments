from django.urls import path

from .views import *

urlpatterns = [
    path("", CommentBase.as_view(), name='main'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]

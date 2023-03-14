from django.urls import path

from .views import *

urlpatterns = [
    # path("login/", LoginUser.as_view(), name="login"),
    path("", CommentBase.as_view(), name='main'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]

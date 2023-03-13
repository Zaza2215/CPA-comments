from django.urls import path

from .views import CommentListView

urlpatterns = [
    # path("login/", LoginUser.as_view(), name="login"),
    path("", CommentListView.as_view())
]

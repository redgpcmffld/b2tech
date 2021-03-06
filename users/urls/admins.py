from django.urls import path

from ..views.admins import SigninView, SignupView

urlpatterns = [
    path('/signup', SignupView.as_view(), name='create_admin'),
    path('/signin', SigninView.as_view(), name='create_token'),
]
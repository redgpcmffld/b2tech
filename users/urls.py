from django.urls import path

from .views import DriverView, SignupView, SigninView

urlpatterns = [
    path('/signup', SignupView.as_view(), name='create_admin'),
    path('/signin', SigninView.as_view(), name='create_token'),
    path('/drivers/<int:driver_id>', DriverView.as_view(), name='delete_driver'),
    path('/drivers', DriverView.as_view(), name='read_drivers|update_driver|create_driver')
]
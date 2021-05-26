from django.urls import path

from ..views.driver_view import DriverView

urlpatterns = [
    path('/<int:driver_id>', DriverView.as_view(), name='delete_driver'),
    path('', DriverView.as_view(), name='read_drivers|update_driver|create_driver')
]

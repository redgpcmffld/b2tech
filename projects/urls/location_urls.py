from django.urls import path

from projects.views.location_view import LocationView

urlpatterns = [
    path('/<int:location_id>', LocationView.as_view(), name='delete_location'),
    path('', LocationView.as_view(), name='create_location|update_location|read_location')
]

from django.urls import path
from .views import CarView, CarListView, SiteView, LocationView

urlpatterns = [
    path('/car-lists', CarListView.as_view()),
    path('/cars/<int:car_id>', CarView.as_view()),
    path('/cars', CarView.as_view()),
    path('/sites/<int:site_id>', SiteView.as_view(), name='delete_site'),
    path('/sites', SiteView.as_view(), name='create_site|update_site|read_site'),
    path('/locations/<int:location_id>', LocationView.as_view(), name='delete_location'),
    path('/locations', LocationView.as_view(), name='create_location|update_location|read_location')
]

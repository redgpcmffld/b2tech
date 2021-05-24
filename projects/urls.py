from django.urls import path
from .views import SiteView, LocationView

urlpatterns = [
    path('/sites/<int:site_id>', SiteView.as_view()),
    path('/sites', SiteView.as_view()),
    path('/locations/<int:location_id>', LocationView.as_view(), name='delete_location'),
    path('/locations', LocationView.as_view(), name='create_location|update_location|read_location')
]

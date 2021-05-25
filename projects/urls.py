from django.urls import path

from .views import (
    ResourceView,
    ResourceTypeView,
    CarView,
    CarTypeView,
    SiteView,
    LocationView,
    ProjectSiteView
)

urlpatterns = [
    path('/list', ProjectSiteView.as_view(), name='read_project_site_list'),
    path('/resources/types', ResourceTypeView.as_view(), name='resource_types_list'),
    path('/resources/<int:resource_id>', ResourceView.as_view(), name='delete_resource'),
    path('/resources', ResourceView.as_view(), name='create_resource|update_resource|read_resource'),
    path('/cars/types', CarTypeView.as_view(), name='car_types_list'),
    path('/cars/<int:car_id>', CarView.as_view(), name='delete_car'),
    path('/cars', CarView.as_view(), name='create_car|update_car|read_car'),
    path('/sites/<int:site_id>', SiteView.as_view(), name='delete_site'),
    path('/sites', SiteView.as_view(), name='create_site|update_site|read_site'),
    path('/locations/<int:location_id>', LocationView.as_view(), name='delete_location'),
    path('/locations', LocationView.as_view(), name='create_location|update_location|read_location')
]

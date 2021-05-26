from django.urls import path, include

urlpatterns = [
    path('projects', include('projects.urls.project_urls')),
    path('projects/sites', include('projects.urls.site_urls')),
    path('projects/resources', include('projects.urls.resource_urls')),
    path('projects/cars', include('projects.urls.car_urls')),
    path('projects/locations', include('projects.urls.location_urls')),

    path('drives', include('records.urls.drive_urls')),

    path('users', include('users.urls.admin_urls')),
    path('users/drivers', include('users.urls.driver_urls'))
]

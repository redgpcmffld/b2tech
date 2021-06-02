from django.urls import path, include

urlpatterns = [
    path('projects', include('projects.urls.projects')),
    path('projects/sites', include('projects.urls.sites')),
    path('projects/resources', include('projects.urls.resources')),
    path('projects/cars', include('projects.urls.cars')),
    path('projects/locations', include('projects.urls.locations')),

    path('records', include('records.urls.drive_records')),

    path('users', include('users.urls.admins')),
    path('users/drivers', include('users.urls.drivers'))
]

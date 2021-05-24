from django.urls import path, include

urlpatterns = [
    path('projects', include('projects.urls')),
<<<<<<< HEAD
=======
    path('users', include('users.urls')),
    path('drives', include('records.urls')),
>>>>>>> develop
]

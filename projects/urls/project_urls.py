from django.urls import path, include

from projects.views.project_view import ProjectSiteView

urlpatterns = [
    path('', ProjectSiteView.as_view(), name='read_project_sites')
]

from django.urls import path

from projects.views.projects import ProjectSiteView
from projects.views.progress import ProgressView, WorkLoadsView

urlpatterns = [
    path('', ProjectSiteView.as_view(), name='read_project_sites'),
    path('/<int:site_id>/workloads', WorkLoadsView.as_view(), name='read_workloads'),
    path('/progress', ProgressView.as_view(), name='read_progress'),
    path('/workloads', WorkLoadsView.as_view(), name='read_workloads'),
]

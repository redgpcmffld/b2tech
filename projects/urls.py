from django.urls import path
from .views import ResourceView, ResourceListView

urlpatterns = [
    path('/resources/<int:resource_id>', ResourceView.as_view()),
    path('/resources', ResourceView.as_view()),
    path('/resource-lists', ResourceListView.as_view()),
]
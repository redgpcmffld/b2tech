from django.urls import path

from projects.views.resource_view import ResourceTypeView, ResourceView, ResourceBlockView

urlpatterns = [
    path('/blocks', ResourceBlockView.as_view(), name='resource_types_list'),
    path('/types', ResourceTypeView.as_view(), name='resource_types_list'),
    path('/<int:resource_id>', ResourceView.as_view(), name='delete_resource'),
    path('', ResourceView.as_view(), name='create_resource|update_resource|read_resource')
]

from django.urls import path

from projects.views.sites import SiteView, SiteListExportView

urlpatterns = [
    path('/<int:site_id>', SiteView.as_view(), name='delete_site'),
    path('', SiteView.as_view(), name='create_site|update_site|read_site'),
    path('/export', SiteListExportView.as_view())
]

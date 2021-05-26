from django.urls import path

from projects.views.site_view import SiteView

urlpatterns = [
    path('/<int:site_id>', SiteView.as_view(), name='delete_site'),
    path('', SiteView.as_view(), name='create_site|update_site|read_site')
]

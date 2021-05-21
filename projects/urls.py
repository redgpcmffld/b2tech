from django.urls import path
from .views import SiteView

urlpatterns = [
    path('/sites/<int:site_id>', SiteView.as_view()),
    path('/sites', SiteView.as_view())
]

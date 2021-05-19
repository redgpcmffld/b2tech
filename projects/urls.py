from django.urls    import path
from .views import LocationView

urlpatterns = [
    path('/locations', LocationView.as_view())
]

from django.urls    import path
from .views import LocationView

urlpatterns = [
    path('/locations/<int:location_id>', LocationView.as_view()),
    path('/locations', LocationView.as_view())
]

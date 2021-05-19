from django.urls import path
from .views import CarView, CarListView

urlpatterns = [
    path('/cars', CarView.as_view()),
    path('/car-lists', CarListView.as_view()),
]

from django.urls import path
from .views import CarView, CarListView

urlpatterns = [
    path('/car-lists', CarListView.as_view()),
    path('/cars/<int:car_id>', CarView.as_view()),
    path('/cars', CarView.as_view())
]

from django.urls import path

from projects.views.cars import CarTypeView, CarView, CarListExportView

urlpatterns = [
    path('/types', CarTypeView.as_view(), name='car_types_list'),
    path('/<int:car_id>', CarView.as_view(), name='delete_car'),
    path('', CarView.as_view(), name='create_car|update_car|read_car'),
    path('/export', CarListExportView.as_view())
]

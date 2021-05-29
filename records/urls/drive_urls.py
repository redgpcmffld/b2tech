from django.urls import path
from ..views.drive_route_view import DriveRouteView
from ..views.dirve_record_view import DriveRecordView, DriveStartView, DriveEndView
from ..views.progress_view import ProgressView, WorkLoadsView

urlpatterns = [
    path('/<int:drive_record_id>', DriveRecordView.as_view(), name='read_drive_record_detail'),
    path('', DriveRecordView.as_view(), name='read_drive_record_list'),
    path('/start', DriveStartView.as_view(), name='create_drive_record'),
    path('/end', DriveEndView.as_view(), name='update_drive_record'),
    path('/progress', ProgressView.as_view(), name='read_progress'),
    path('/routes/<int:drive_record_id>', DriveRouteView.as_view(), name='read_drive_route_detail'),
    path('/routes', DriveRouteView.as_view(), name='create_drive_route|read_drive_routes'),
    path('/workloads', WorkLoadsView.as_view(), name='read_workloads')
]

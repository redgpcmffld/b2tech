from django.urls import path
from ..views.drive_route_view import DriveRouteView
from ..views.dirve_record_view import DriveRecordView, DriveStartView, DriveEndView, GraphView
from ..views.progress_view import ProgressView

urlpatterns = [
    path('/graph', GraphView.as_view()),
    path('/<int:drive_record_id>', DriveRecordView.as_view(), name='read_drive_record_detail'),
    path('', DriveRecordView.as_view(), name='read_drive_record_list'),
    path('/start', DriveStartView.as_view(), name='create_drive_record'),
    path('/end', DriveEndView.as_view(), name='update_drive_record'),
    path('/progress', ProgressView.as_view(), name='read_progress'),
    path('/routes', DriveRouteView.as_view(), name='create_drive_route')
]

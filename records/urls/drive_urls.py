from django.urls import path
from ..views.dirve_record_view import DriveRecordView, DriveRecordDetailView, DriveRecordListExportView
from ..views.progress_view import ProgressView, WorkLoadsView

urlpatterns = [
    path('/<int:drive_record_id>/details', DriveRecordDetailView.as_view(), name='create_drive_route|read_drive_routes'),
    path('/details', DriveRecordDetailView.as_view(), name='read_all_drive_routes'),
    path('/<int:drive_record_id>', DriveRecordView.as_view(), name='read_drive_record_detail|update_drive_record'),
    path('', DriveRecordView.as_view(), name='read_drive_record_list|create_drive_record'),
    path('/progress', ProgressView.as_view(), name='read_progress'),
    path('/workloads', WorkLoadsView.as_view(), name='read_workloads'),
    path('/export', DriveRecordListExportView.as_view())
]

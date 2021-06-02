from django.urls import path
from ..views.drive_records import DriveRecordView, DriveRouteView, DriveRecordListExportView

urlpatterns = [
    path('/<int:drive_record_id>/routes', DriveRouteView.as_view(), name='create_drive_route|read_drive_routes'),
    path('/all/routes', DriveRouteView.as_view(), name='read_all_drive_routes'),
    path('/<int:drive_record_id>', DriveRecordView.as_view(), name='read_drive_record_detail|update_drive_record'),
    path('', DriveRecordView.as_view(), name='read_drive_record_list|create_drive_record'),
    path('/export', DriveRecordListExportView.as_view())
]

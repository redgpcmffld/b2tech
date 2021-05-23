from django.urls    import path
from .views import DriveStartView, DriveRecordView, DriveEndView

urlpatterns = [
    path('/<int:drive_record_id>', DriveRecordView.as_view(), name='read_drive_record_detail'),
    path('', DriveRecordView.as_view(), name='read_drive_record_list'),
    path('/start', DriveStartView.as_view(), name='create_drive_record'),
    path('/end', DriveEndView.as_view(), name='update_drive_record')
]
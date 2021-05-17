from django.db import models


class DriveRecord(models.Model):
    drive_record_id = models.BigAutoField(primary_key=True)
    car = models.ForeignKey('projects.Car', on_delete=models.SET_NULL, null=True)
    loading_location = models.ForeignKey('projects.Location', on_delete=models.SET_NULL, null=True,
                                         related_name='loading_location')
    unloading_location = models.ForeignKey('projects.Location', on_delete=models.SET_NULL, null=True,
                                           related_name='unloading_location')
    transport_weight = models.IntegerField()
    loading_time = models.DateTimeField()
    unloading_time = models.DateTimeField()
    driving_date = models.DateField()
    total_distance = models.DecimalField(max_digits=10, decimal_places=4)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'drive_records'


class DriveRoute(models.Model):
    drive_route_id = models.BigAutoField(primary_key=True)
    latitude = models.DecimalField(max_digits=15,decimal_places=12)
    longitude = models.DecimalField(max_digits=15,decimal_places=12)
    distance = models.DecimalField(max_digits=10, decimal_places=4)
    drive_record = models.ForeignKey(DriveRecord, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'drive_routes'

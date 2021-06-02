from django.db import models

from projects.models.cars import Car
from users.models.drivers import Driver
from projects.models.locations import Location


class DriveRecord(models.Model):
    STATUS = ((1, '상차'), (2, '정상종료'), (3, '강제하차승인요청'), (4, '강제하차확인'))
    drive_record_id = models.BigAutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    loading_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True,
                                         related_name='loading_location')
    unloading_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True,
                                           related_name='unloading_location')
    transport_weight = models.IntegerField()
    loading_time = models.DateTimeField()
    unloading_time = models.DateTimeField(null=True)
    driving_date = models.DateField()
    total_distance = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    status = models.SmallIntegerField(default=1, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'drive_records'

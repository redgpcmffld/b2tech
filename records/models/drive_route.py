from django.db import models

from rest_framework import serializers

from .drive_record import DriveRecord


class DriveRoute(models.Model):
    drive_route_id = models.BigAutoField(primary_key=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=12)
    longitude = models.DecimalField(max_digits=15, decimal_places=12)
    distance = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    drive_record = models.ForeignKey(DriveRecord, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'drive_routes'


class DriveRouteSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(max_digits=15, decimal_places=12)
    longitude = serializers.DecimalField(max_digits=15, decimal_places=12)

    class Meta:
        model = DriveRoute
        fields = '__all__'


class DriveRouteViewSerializer(serializers.Serializer):
    class Meta:
        model = DriveRecord
        fields = [
            'latitude',
            'longitude'
        ]

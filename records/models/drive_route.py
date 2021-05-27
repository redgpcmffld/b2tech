from django.db import models

from rest_framework import serializers
from haversine import haversine

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

    def create(self, validated_data):
        if not DriveRecord.objects.get(pk=validated_data['drive_record'].pk).driveroute_set.filter(
                is_active=True).exists():
            validated_data['distance'] = 0
            instance = DriveRoute.objects.create(**validated_data)
            return instance
        elif DriveRecord.objects.get(pk=validated_data['drive_record'].pk).driveroute_set.filter(
                is_active=True).count() > 1:
            drive_route = DriveRecord.objects.get(pk=validated_data['drive_record'].pk).driveroute_set.last()
        else:
            drive_route = DriveRecord.objects.get(pk=validated_data['drive_record'].pk).driveroute_set.get()
        float_formatter = "{0:.4f}"
        validated_data['distance'] = float_formatter.format(haversine((drive_route.longitude, drive_route.latitude), (
            validated_data['longitude'], validated_data['latitude']), unit='km'))
        instance = DriveRoute.objects.create(**validated_data)
        return instance


class DriveRouteViewSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    loading_location = serializers.SerializerMethodField(method_name='get_loading_location')
    unloading_location = serializers.SerializerMethodField(method_name='get_unloading_location')
    drive_route = serializers.SerializerMethodField(method_name='get_drive_route_info')

    class Meta:
        model = DriveRecord
        fields = [
            'pk',
            'drive_route'
        ]

    def get_loading_location(self, drive_record):
        loading_location = drive_record.loading_location
        result = {
            'pk': loading_location.pk,
            'type': loading_location.type,
            'name': loading_location.name,
            'longitude': loading_location.longitude,
            'latitude': loading_location.latitude
        }
        return result

    def get_unloading_location(self, drive_record):
        unloading_location = drive_record.unloading_location
        result = {
            'pk': unloading_location.pk,
            'type': unloading_location.type,
            'name': unloading_location.name,
            'longitude': unloading_location.longitude,
            'latitude': unloading_location.latitude
        }
        return result

    def get_drive_route_info(self, drive_record):
        result = [
            {
                'pk': drive_route['pk'],
                'longitude': drive_route['longitude'],
                'latitude': drive_route['latitude']
            }
            for drive_route in drive_record.driveroute_set.values('pk', 'longitude', 'latitude') if not None]
        return result

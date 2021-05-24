from datetime import datetime, date
from django.db.models import Sum

from rest_framework import serializers

from projects.models import Location, Car
from .models import DriveRecord, DriveRoute


class DriveRecordViewSerializer(serializers.ModelSerializer):
    resource = serializers.SerializerMethodField(method_name='get_resource_name')
    loading_time = serializers.SerializerMethodField(method_name='get_loading_time')
    unloading_time = serializers.SerializerMethodField(method_name='get_unloading_time')
    driving_date = serializers.SerializerMethodField(method_name='get_driving_date')
    loading_location = serializers.SlugRelatedField(slug_field='name', read_only=True)
    unloading_location = serializers.SlugRelatedField(slug_field='name', read_only=True)
    transport_weight = serializers.SerializerMethodField(method_name='get_transport_weight')
    car = serializers.SerializerMethodField(method_name='get_car_driver_name')
    status = serializers.SerializerMethodField(method_name='get_status_name')

    class Meta:
        model = DriveRecord
        fields = [
            'car',
            'loading_location',
            'unloading_location',
            'loading_time',
            'unloading_time',
            'transport_weight',
            'driving_date',
            'total_distance',
            'status',
            'resource'
        ]

    def get_resource_name(self, obj):
        result = {
            'pk': obj.loading_location.resource.get().pk,
            'name': obj.loading_location.resource.get().name
        }
        return result

    def get_loading_time(self, obj):
        result = obj.loading_time.strftime('%y년 %m월 %d일 %H시 %M분')
        return result

    def get_unloading_time(self, obj):
        result = obj.loading_time.strftime('%y년 %m월 %d일 %H시 %M분')
        return result

    def get_driving_date(self, obj):
        result = obj.loading_time.strftime('%y년 %m월 %d일')
        return result

    def get_transport_weight(self, obj):
        result = f'{obj.transport_weight}{obj.loading_location.resource.get().block}'
        return result

    def get_car_driver_name(self, obj):
        result = {
            'number': obj.car.number,
            'driver_name': obj.car.driver.name
        }
        return result

    def get_status_name(self, obj):
        STATUS = ('상차', '정상종료', '강제하차승인요청' '강제하차확인')
        return STATUS[obj.status - 1]


class DriveStartSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(required=True, queryset=Car.objects.filter(is_active=True))
    loading_location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.filter(is_active=True, type=True), required=True)
    unloading_location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.filter(is_active=True, type=False), required=True)
    loading_time = serializers.DateTimeField(default=datetime.now())
    transport_weight = serializers.IntegerField()
    driving_date = serializers.DateField(default=date.today())
    status = serializers.IntegerField(max_value=4, min_value=1, default=1)

    class Meta:
        model = DriveRecord
        fields = [
            'car',
            'loading_location',
            'unloading_location',
            'loading_time',
            'transport_weight',
            'driving_date',
            'status'
        ]


class DriveEndSerializer(serializers.ModelSerializer):
    unloading_time = serializers.DateTimeField(default=datetime.now())
    status = serializers.IntegerField(max_value=4, min_value=1)
    total_distance = serializers.SerializerMethodField(method_name='get_total_distance')

    class Meta:
        model = DriveRecord
        fields = [
            'unloading_time',
            'status',
            'total_distance'
        ]

    def get_total_distance(self, obj):
        result = obj.driveroute_set.aggregate(Sum('distance'))['distance__sum']
        return result

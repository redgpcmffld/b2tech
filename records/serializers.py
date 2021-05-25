from datetime import datetime, date, timedelta
from django.db.models import Sum, Min, Max, Avg, When, F, Q

from rest_framework import serializers

from projects.models import Project, Site, Location, Car
from users.models import Admin
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
            'drive_record_id',
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
        obj.total_distance = result
        return obj.total_distance


class ProgressSerializer(serializers.Serializer):
    site_id = serializers.IntegerField(read_only=True)
    site_name = serializers.SerializerMethodField(method_name='get_site_name')
    progress = serializers.SerializerMethodField(method_name='get_progress')
    site_coordinate = serializers.SerializerMethodField(method_name='get_site_coordinate')

    class Meta:
        model = Site
        fields = [
            'site_id',
            'site_name',
            'percent',
            'weight',
            'site_coordinate'
        ]

    def get_progress(self, obj):
        site_max_plan = self.instance.annotate(site_plan=Sum('location__plan')).aggregate(Max('site_plan'))[
            'site_plan__max']
        plan = obj.location_set.aggregate(Sum('plan'))['plan__sum']
        site_plan = int(plan / site_max_plan * 5)
        today_workloads = obj.location_set.filter(is_active=True).aggregate(
            today_workloads=Sum('loading_location__transport_weight',
                                filter=Q(loading_location__driving_date=date.today()) & Q(loading_location__status=2)))[
            'today_workloads']
        days = (date.fromisoformat(obj.end_date) - date.fromisoformat(obj.start_date)).days
        today_plan = plan // days
        if today_workloads is None:
            today_workloads = 0
        progress = int(today_workloads / today_plan * 5)
        if progress == 0:
            progress = 1
        if site_plan == 0:
            site_plan = 1
        result = {
            'weight': site_plan,
            'percent': progress
        }

        return result

    def get_site_coordinate(self, obj):
        site_coordinates = obj.location_set.filter(is_active=True).aggregate(Min('longitude'), Max('longitude'),
                                                                             Min('latitude'), Max('latitude'))
        if site_coordinates['longitude__min'] and \
                site_coordinates['longitude__max'] and \
                site_coordinates['latitude__min'] and \
                site_coordinates['latitude__max'] is None:
            return {'longitude': 0, 'latitude': 0}
        result = {
            'longitude': (site_coordinates['longitude__min'] +
                          (site_coordinates['longitude__max'] - site_coordinates['longitude__min'])
                          // 2),
            'latitude': (site_coordinates['latitude__min'] +
                         (site_coordinates['latitude__max'] - site_coordinates['latitude__min'])
                         // 2)
        }
        return result

    def get_site_name(self, obj):
        return obj.name

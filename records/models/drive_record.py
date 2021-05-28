from datetime import date, datetime

from django.db import models
from django.db.models import Q

from rest_framework import serializers

from projects.models.car import Car
from projects.models.location import Location
from projects.models.site import Site


class DriveRecord(models.Model):
    STATUS = ((1, '상차'), (2, '정상종료'), (3, '강제하차승인요청'), (4, '강제하차확인'))
    drive_record_id = models.BigAutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
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
    total_distance = serializers.SerializerMethodField(method_name='get_total_distance')

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

    def get_total_distance(self, obj):
        if obj.total_distance is None:
            obj.total_distance = "%.4f" % 0
        return f'{obj.total_distance}km'


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

    def validate(self, data):
        admin = self.context.get('admin')
        car_pk = self.context.get('car_pk')
        loading_location = data['loading_location']
        unloading_location = data['unloading_location']
        q = Q(is_active=True)
        if admin.type == 'ProjectTotalAdmin':
            q.add(Q(project__project_admin__pk=admin.pk), q.AND)
            loading_location_site_check = Site.objects.filter(q, location__pk=loading_location.pk).exists()
            unloading_location_site_check = Site.objects.filter(q, location__pk=unloading_location.pk).exists()
            car_site_check = Site.objects.filter(q, car__pk=car_pk).exists()
            if not (loading_location_site_check or unloading_location_site_check or car_site_check):
                raise serializers.ValidationError('INVALID_LOCATION')
        elif admin.type == 'SiteAdmin':
            q.add(Q(site_admin__pk=admin.pk), q.AND)
            loading_location_site_check = Site.objects.filter(q, location__pk=loading_location.pk).exists()
            unloading_location_site_check = Site.objects.filter(q, location__pk=unloading_location.pk).exists()
            car_site_check = Site.objects.filter(q, car__pk=car_pk).exists()
            if not (loading_location_site_check or unloading_location_site_check or car_site_check):
                raise serializers.ValidationError('INVALID_LOCATION')

        if loading_location.resource.get(is_active=True).pk != unloading_location.resource.get(is_active=True).pk:
            raise serializers.ValidationError('INVALID_LOCATION_RESOURCE')
        return data


class DriveEndSerializer(serializers.ModelSerializer):
    unloading_time = serializers.DateTimeField(default=datetime.now())
    status = serializers.IntegerField(max_value=4, min_value=1)

    class Meta:
        model = DriveRecord
        fields = [
            'unloading_time',
            'status',
            'total_distance'
        ]

from datetime import date, datetime

from django.db.models import Q, Sum

from rest_framework import serializers

from ..models.drive_records import DriveRecord
from projects.models.sites import Site
from projects.models.locations import Location
from projects.models.cars import Car
from users.models.drivers import Driver


class DriveRecordViewSerializer(serializers.ModelSerializer):
    resource = serializers.SerializerMethodField(method_name='get_resource_name')
    loading_time = serializers.SerializerMethodField(method_name='get_loading_time')
    unloading_time = serializers.SerializerMethodField(method_name='get_unloading_time')
    driving_date = serializers.SerializerMethodField(method_name='get_driving_date')
    loading_location = serializers.SlugRelatedField(slug_field='name', read_only=True)
    unloading_location = serializers.SlugRelatedField(slug_field='name', read_only=True)
    transport_weight = serializers.SerializerMethodField(method_name='get_transport_weight')
    car = serializers.SlugRelatedField(slug_field='number', read_only=True)
    driver = serializers.SlugRelatedField(slug_field='name', read_only=True)
    status = serializers.SerializerMethodField(method_name='get_status_name')
    total_distance = serializers.SerializerMethodField(method_name='get_total_distance')

    class Meta:
        model = DriveRecord
        fields = [
            'drive_record_id',
            'car',
            'driver',
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

    def get_resource_name(self, drive_record):
        return drive_record.loading_location.resource.get(is_active=True).name

    def get_loading_time(self, drive_record):
        return drive_record.loading_time.strftime('%y년 %m월 %d일 %H시 %M분')

    def get_unloading_time(self, drive_record):
        return drive_record.loading_time.strftime('%y년 %m월 %d일 %H시 %M분')

    def get_driving_date(self, drive_record):
        return drive_record.loading_time.strftime('%y년 %m월 %d일')

    def get_transport_weight(self, drive_record):
        return f'{drive_record.transport_weight}{drive_record.loading_location.resource.get(is_active=True).block}'

    def get_status_name(self, drive_record):
        STATUS = ('상차', '정상종료', '강제하차승인요청' '강제하차확인')
        return STATUS[drive_record.status - 1]

    def get_total_distance(self, drive_record):
        if drive_record.total_distance is None:
            drive_record.total_distance = "%.4f" % 0
        return f'{drive_record.total_distance}km'


class DriveRecordCreateSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(required=True, queryset=Car.objects.filter(is_active=True))
    driver = serializers.PrimaryKeyRelatedField(required=True, queryset=Driver.objects.filter(is_active=True))
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
            'drive_record_id',
            'car',
            'driver',
            'loading_location',
            'unloading_location',
            'loading_time',
            'transport_weight',
            'driving_date',
            'status'
        ]

    def validate(self, data):
        admin = self.context['admin']
        car_pk = self.context['car_pk']
        driver_pk = self.context['driver_pk']
        loading_location = data['loading_location']
        unloading_location = data['unloading_location']
        q = Q(is_active=True)
        if admin.type == 'ProjectTotalAdmin':
            q.add(Q(project__project_admin__pk=admin.pk), q.AND)
            loading_location_site_check = Site.objects.filter(q, location__pk=loading_location.pk).exists()
            unloading_location_site_check = Site.objects.filter(q, location__pk=unloading_location.pk).exists()
            car_site_check = Site.objects.filter(q, car__pk=car_pk).exists()
            driver_site_check = Site.objects.filter(q, driver__pk=driver_pk).exists()
            if loading_location_site_check and unloading_location_site_check and car_site_check and driver_site_check:
                if loading_location.resource.get(is_active=True).pk != unloading_location.resource.get(
                        is_active=True).pk:
                    raise serializers.ValidationError('INVALID_LOCATION_RESOURCE')
                return data
            raise serializers.ValidationError('INVALID_DATA')
        elif admin.type == 'SiteAdmin':
            q.add(Q(site_admin__pk=admin.pk), q.AND)
            loading_location_site_check = Site.objects.filter(q, location__pk=loading_location.pk).exists()
            unloading_location_site_check = Site.objects.filter(q, location__pk=unloading_location.pk).exists()
            car_site_check = Site.objects.filter(q, car__pk=car_pk).exists()
            driver_site_check = Site.objects.filter(q, driver__pk=driver_pk).exists()
            if loading_location_site_check and unloading_location_site_check and car_site_check and driver_site_check:
                if loading_location.resource.get(is_active=True).pk != unloading_location.resource.get(
                        is_active=True).pk:
                    raise serializers.ValidationError('INVALID_LOCATION_RESOURCE')
                return data
            raise serializers.ValidationError('INVALID_DATA')


class DriveRecordUpdateSerializer(serializers.ModelSerializer):
    unloading_time = serializers.DateTimeField(default=datetime.now())
    status = serializers.IntegerField(max_value=4, min_value=1)

    class Meta:
        model = DriveRecord
        fields = [
            'drive_record_id',
            'unloading_time',
            'status',
            'total_distance'
        ]

    def update(self, instance, validated_data):
        validated_data['total_distance'] = instance.driveroute_set.filter(is_active=True).aggregate(
            total_distance=Sum('distance'))['total_distance']

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

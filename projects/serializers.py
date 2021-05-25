from django.core import validators
from rest_framework import serializers

from .models import Location, Resource, Project, Site, Car
from users.models import Driver, Admin


class SiteAdminViewSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ['pk', 'name', 'project']

    def get_project(self, obj):
        return {'project_id': obj.project.pk}


class ProjectViewSerializer(serializers.ModelSerializer):
    site_set = SiteAdminViewSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['pk', 'name', 'site_set']

    def get_site(self, obj):
        return {'site_id': obj.site.pk, 'name': obj.site.name}


class CarSerializer(serializers.ModelSerializer):
    site = serializers.PrimaryKeyRelatedField(queryset=Site.objects.filter(is_active=True))
    driver = serializers.PrimaryKeyRelatedField(many=True, queryset=Driver.objects.filter(is_active=True))

    class Meta:
        model = Car
        fields = '__all__'

    def validate_number(self, attrs):
        if Car.objects.filter(number=attrs):
            raise validators.ValidationError('DUPLICATE_NUMBER')

        validators.RegexValidator(r'^[가-힣]{2}\d{2}[가-힣]{1}\d{4}$', 'INVALID_NUMBER')(attrs)
        return attrs


class CarViewSerializer(serializers.ModelSerializer):
    site = serializers.SerializerMethodField()
    driver = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['type', 'number', 'driver', 'site']

    def get_site(self, obj):
        return {'site_id': obj.site.pk, 'name': obj.site.name}

    def get_driver(self, obj):
        return {'driver_id': obj.driver.get().pk, 'phone_number': obj.driver.get().phone_number,
                'name': obj.driver.get().name}


class MyDateField(serializers.DateField):

    def to_internal_value(self, value):
        return f'{value}-01'


class SiteSerializer(serializers.ModelSerializer):
    start_date = MyDateField()
    end_date = MyDateField()

    class Meta:
        model = Site
        fields = '__all__'

    def validate_name(self, attrs):
        validators.RegexValidator(r'^[가-힣a-zA-Z0-9\s]{1,50}$', 'INVALID_NAME')(attrs)
        return attrs


class SiteViewSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ['name', 'start_date', 'end_date', 'project']

    def get_project(self, obj):
        return {'project_id': obj.project.pk, 'name': obj.project.name}


class LocationSerializer(serializers.ModelSerializer):
    resource = serializers.PrimaryKeyRelatedField(many=True, queryset=Resource.objects.filter(is_active=True),
                                                  required=True)

    class Meta:
        model = Location
        fields = '__all__'


class LocationViewSerializer(serializers.ModelSerializer):
    site = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = [
            'location_id',
            'site',
            'type',
            'name',
            'address',
            'latitude',
            'longitude',
            'range',
            'is_allow'
        ]

    def get_site(self, obj):
        return {'site_id': obj.site.get().pk, 'name': obj.site.get().name}


class LocationResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_id', 'name']


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class ResourceViewSerializer(serializers.ModelSerializer):
    location_set = LocationResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Resource
        fields = ['pk', 'name', 'type', 'block', 'location_set']

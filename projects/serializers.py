from rest_framework import serializers

from .models import Car, Site, Location, Resource
from users.models import Driver
from django.core import validators


class CarSerializer(serializers.ModelSerializer):
    site = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())
    driver = serializers.PrimaryKeyRelatedField(many=True, queryset=Driver.objects.all())

    class Meta:
        model = Car
        fields = '__all__'

    def validate_number(self, attrs):
        validators.RegexValidator(r'^[가-힣]{2}\d{2}[가-힣]{1}\d{4}$', 'INVALID_NUMBER')(attrs)
        return attrs


class CarViewSerializer(serializers.ModelSerializer):
    driver = serializers.SerializerMethodField()
    site = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['type', 'number', 'driver', 'site']

    def get_site(self, obj):
        return {'site_id': obj.site.pk, 'name': obj.site.name}

    def get_driver(self, obj):
        return {'driver_id': obj.driver.get().pk, 'phone_number': obj.driver.get().phone_number,
                'name': obj.driver.get().name}


class LocationSerializer(serializers.ModelSerializer):
    resource = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all(), required=True)

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
            'is_allow',
        ]

    def get_site(self, obj):
        return {'site_id': obj.site.pk, 'name': obj.site.name}


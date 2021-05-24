from django.core import validators
from django.db.models import Sum

from rest_framework import serializers

from .models import Site, Location, Resource


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

    def validate_name(self, attrs):
        if Site.objects.filter(name=attrs).exists():
            raise validators.ValidationError('DUPLICATE_NAME')

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

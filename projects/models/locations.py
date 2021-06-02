from django.db import models

from rest_framework import serializers

from projects.models.sites import Site


class Location(models.Model):
    from projects.models.resources import Resource
    location_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    site = models.ManyToManyField(Site)
    longitude = models.DecimalField(max_digits=15, decimal_places=12)
    latitude = models.DecimalField(max_digits=15, decimal_places=12)
    type = models.BooleanField()
    resource = models.ManyToManyField(Resource)
    plan = models.IntegerField()
    range = models.IntegerField()
    is_allow = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'locations'


class LocationCreateSerializer(serializers.ModelSerializer):
    from projects.models.resources import Resource
    resource = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Resource.objects.filter(is_active=True),
        required=True
    )

    class Meta:
        model = Location
        fields = '__all__'


class LocationViewSerializer(serializers.ModelSerializer):
    site = serializers.SerializerMethodField(method_name='get_site_info')
    resource = serializers.SerializerMethodField(method_name='get_resource_info')

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
            'resource',
            'plan',
            'range',
            'is_allow'
        ]

    def get_site_info(self, location):
        return [
            {
                'site_id': site.pk,
                'name': site.name
            }
            for site in location.site.filter(is_active=True)]

    def get_resource_info(self, location):
        return [
            {
                'resource_id': resource.pk,
                'name': resource.name
            }
        for resource in location.resource.filter(is_active=True)]

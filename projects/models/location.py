from django.db import models

from rest_framework import serializers

from projects.models.site import Site


class Location(models.Model):
    from projects.models.resource import Resource
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


class LocationSerializer(serializers.ModelSerializer):
    from projects.models.resource import Resource
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

from rest_framework import serializers

from .models import Location, Resource


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

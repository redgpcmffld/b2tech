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
            'is_allow'
        ]

    def get_site(self, obj):
        return {'site_id': obj.site.pk, 'name': obj.site.name}


from django.db.models import Sum

from rest_framework import serializers

from .models import Location, Resource, Site


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

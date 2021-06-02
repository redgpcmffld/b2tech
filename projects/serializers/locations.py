from rest_framework import serializers

from ..models.locations import Location


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

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
            'resource',
            'plan'
        ]

    def get_site(self, obj):
        return {'site_id': obj.site.pk, 'name': obj.site.name}
    #
    # def get_type(self, obj):
    #     if obj.type == 1:
    #         obj.type = '상차지'
    #     else:
    #         obj.type = '하차지'
    #     return obj.type

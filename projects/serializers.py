from rest_framework import serializers

from .models import Location, Resource

class LocationSerializer(serializers.ModelSerializer):
    resource = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all(), required=True)
    class Meta:
        model = Location
        fields = '__all__'

class LocationViewSerializer(serializers.ModelSerializer):
    site = serializers.SerializerMethodField()
    type = serializers.CharField(max_length=3)
    range = serializers.CharField(max_length=10)

    class Meta:
        model = Location
        fields = ['site', 'type', 'name', 'address', 'latitude', 'longitude', 'range', 'is_allow']

    def get_site_name(self, obj):
        return obj.site.name

    def get_type(self, attrs):
        if attrs == 1:
            attrs = '상차지'
        else:
            attrs = '하차지'
        return attrs

    def get_range(self, attrs):
        return f'{attrs}m'

from rest_framework import serializers

from .models import Location, Resource

class LocationSerializer(serializers.ModelSerializer):
    resource = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all(), required=True)
    class Meta:
        model = Location
        fields = '__all__'

class LocationViewSerializer(serializers.ModelSerializer):
    site = serializers.SerializerMethodField()
    range = serializers.CharField(max_length=10)

    class Meta:
        model = Location
        fields = ['site', 'type', 'name', 'address', 'latitude', 'longitude', 'range', 'is_allow']

    def get_site(self, obj):
        return obj.site.name

    def get_type(self, obj):
        print(obj)
        if obj.type == True:
            obj.type = '상차지'
        else:
            obj.type = '하차지'
        return obj

    def get_range(self, attrs):
        return f'{attrs}m'

    def get_attribute(self, instance):
        print(instance)

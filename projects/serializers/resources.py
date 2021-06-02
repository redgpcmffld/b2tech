from rest_framework import serializers

from ..models.resources import Resource


class ResourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

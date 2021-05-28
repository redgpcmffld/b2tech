from django.db import models

from rest_framework import serializers


class Resource(models.Model):
    BLOCK_UNITS = (('Ton', '톤'), ('Kg', '킬로그램'), ('m**3', '세제곱미터'))
    TYPES = (('Stone', '돌'), ('Iron', '철'), ('Waste', '폐기물'), ('Dirt', '사토'))

    resource_id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=TYPES)
    name = models.CharField(max_length=50)
    block = models.CharField(max_length=10, choices=BLOCK_UNITS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'resources'


class ResourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class ResourceLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['resource_id', 'name', 'type', 'block']


class ResourceViewSerializer(serializers.ModelSerializer):
    resource = ResourceLocationSerializer(many=True, read_only=True)

    class Meta:
        from projects.models.location import Location
        model = Location
        fields = ['location_id', 'name', 'resource']

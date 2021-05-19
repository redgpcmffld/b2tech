from rest_framework import serializers
from .models import Site
from django.core import validators


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

    def validate_name(self, attrs):
        validators.RegexValidator(r'^[가-힣a-zA-Z0-9\s]{1,50}$', 'INVALID_NAME')(attrs)
        return attrs

    def validate_start_date(self, attrs):
        validators.RegexValidator(r'^(19|20)\d{2}-(0[1-9]|1[012])$', 'INVALID_START_DATE')(attrs)
        return attrs

    def validate_end_date(self, attrs):
        validators.RegexValidator(r'^(19|20)\d{2}-(0[1-9]|1[012])$', 'INVALID_END_DATE')(attrs)
        return attrs


class SiteViewSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ['name', 'start_date', 'end_date', 'project']

    def get_project(self, obj):
        return {'project_id': obj.project.pk, 'name': obj.project.name}

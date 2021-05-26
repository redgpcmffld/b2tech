from django.db import models
from django.core import validators

from rest_framework import serializers

from projects.models.project import Project


class Site(models.Model):
    site_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sites'


class MyDateField(serializers.DateField):

    def to_internal_value(self, value):
        return f'{value}-01'


class SiteSerializer(serializers.ModelSerializer):
    start_date = MyDateField()
    end_date = MyDateField()

    class Meta:
        model = Site
        fields = '__all__'

    def validate_name(self, attrs):
        validators.RegexValidator(r'^[가-힣a-zA-Z0-9\s]{1,50}$', 'INVALID_NAME')(attrs)
        return attrs


class SiteViewSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ['name', 'start_date', 'end_date', 'project']

    def get_project(self, obj):
        return {'project_id': obj.project.pk, 'name': obj.project.name}

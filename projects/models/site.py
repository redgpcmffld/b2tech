from django.db import models

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


class SiteCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(input_formats=['%Y-%m'])
    end_date = serializers.DateField(input_formats=['%Y-%m'])

    class Meta:
        model = Site
        fields = '__all__'


class SiteViewSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ['site_id', 'name', 'start_date', 'end_date', 'project']

    def get_project(self, site):
        return {'project_id': site.project.pk, 'name': site.project.name}

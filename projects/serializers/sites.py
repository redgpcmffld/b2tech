from rest_framework import serializers

from ..models.sites import Site


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

from django.core import validators

from rest_framework import serializers

from ..models.drivers import Driver
from projects.models.sites import Site


class DriverViewSerializer(serializers.ModelSerializer):
    site = serializers.SerializerMethodField(method_name='get_site_info')
    created_at = serializers.DateField(write_only=True, required=False)
    updated_at = serializers.DateField(write_only=True, required=False)
    is_active = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = Driver
        fields = '__all__'

    def get_site_info(self, driver):
        return {
            'site_id': driver.site.pk,
            'name': driver.site.name
        }


class DriverCreateSerializer(serializers.ModelSerializer):
    site = serializers.PrimaryKeyRelatedField(queryset=Site.objects.filter(is_active=True), required=True)

    class Meta:
        model = Driver
        fields = '__all__'

    def validate(self, data):
        validators.RegexValidator(r'^\d{11}$', '잘못된 전화번호 형식입니다.')(data.get('phone_number'))
        validators.RegexValidator(r'^[가-힣]{2,}$|^[a-z]{2,20}$', '이름은 2글자 이상 한글이거나 영어이어야 합니다.')(data.get('name'))
        admin = self.context['admin']
        if admin.type == 'ProjectTotalAdmin':
            if not Site.objects.filter(project__project_admin__pk=admin.pk).exists():
                raise serializers.ValidationError('INVALID_SITE')
        elif not Site.objects.filter(site_admin__pk=admin.pk).exists():
            raise serializers.ValidationError('INVALID_SITE')
        return data

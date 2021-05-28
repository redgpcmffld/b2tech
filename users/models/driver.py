from django.db import models

from django.core import validators

from rest_framework import serializers

from projects.models.site import Site


class Driver(models.Model):
    driver_id = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=20)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'drivers'


class DriverViewSerializer(serializers.ModelSerializer):
    site = serializers.SlugRelatedField(read_only=True, slug_field='name')
    created_at = serializers.DateField(write_only=True, required=False)
    updated_at = serializers.DateField(write_only=True, required=False)
    is_active = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = Driver
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    site = serializers.PrimaryKeyRelatedField(queryset=Site.objects.filter(is_active=True), required=True)

    class Meta:
        model = Driver
        fields = '__all__'

    def validate(self, attrs):
        validators.RegexValidator(r'^\d{11}$', '잘못된 전화번호 형식입니다.')(attrs.get('phone_number'))
        validators.RegexValidator(r'^[가-힣]{2,}$|^[a-z]{2,20}$', '이름은 2글자 이상 한글이거나 영어이어야 합니다.')(attrs.get('name'))
        admin = self.context['admin']
        if admin.type == 'ProjectTotalAdmin':
            if Site.objects.filter(project__project_admin__pk=admin.pk).exists():
                raise serializers.ValidationError('INVALID_SITE')
        if Site.objects.filter(site_admin__pk=admin.pk).exists():
            raise serializers.ValidationError('INVALID_SITE')
        return attrs

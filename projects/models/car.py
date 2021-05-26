from django.db import models
from django.core import validators

from rest_framework import serializers

from projects.models.site import Site
from users.models.driver import Driver


class Car(models.Model):
    TYPES = (('DumpTruck', '덤프 트럭'), ('WasteTruck', '폐기물 트럭'), ('RecyclingTruck', '재활용 트럭'), ('Tank', '탱크'))

    car_id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=TYPES)
    number = models.CharField(max_length=20)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    driver = models.ManyToManyField(Driver, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'cars'


class CarSerializer(serializers.ModelSerializer):
    site = serializers.PrimaryKeyRelatedField(queryset=Site.objects.filter(is_active=True))
    driver = serializers.PrimaryKeyRelatedField(many=True, queryset=Driver.objects.filter(is_active=True))

    class Meta:
        model = Car
        fields = '__all__'

    def validate_number(self, attrs):
        validators.RegexValidator(r'^[가-힣]{2}\d{2}[가-힣]{1}\d{4}$', 'INVALID_NUMBER')(attrs)
        return attrs


class CarViewSerializer(serializers.ModelSerializer):
    site = serializers.SerializerMethodField()
    driver = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['type', 'number', 'driver', 'site']

    def get_site(self, obj):
        return {'site_id': obj.site.pk, 'name': obj.site.name}

    def get_driver(self, obj):
        return {'driver_id': obj.driver.get().pk, 'phone_number': obj.driver.get().phone_number,
                'name': obj.driver.get().name}

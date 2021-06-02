from django.core import validators

from rest_framework import serializers

from ..models.cars import Car
from users.models.drivers import Driver




class CarCreateSerializer(serializers.ModelSerializer):
    site = serializers.PrimaryKeyRelatedField(queryset=Site.objects.filter(is_active=True))
    driver = serializers.PrimaryKeyRelatedField(many=True, queryset=Driver.objects.filter(is_active=True))

    class Meta:
        model = Car
        fields = '__all__'

    def validate_number(self, number):
        validators.RegexValidator(r'^[가-힣]{2}\d{2}[가-힣]{1}\d{4}$', 'INVALID_NUMBER')(number)
        return number


class CarViewSerializer(serializers.ModelSerializer):
    site = serializers.SerializerMethodField(method_name='get_site')
    driver = serializers.SerializerMethodField(method_name='get_driver')

    class Meta:
        model = Car
        fields = ['car_id', 'type', 'number', 'driver', 'site']

    def get_site(self, car):
        return {'site_id': car.site.pk, 'name': car.site.name}

    def get_driver(self, car):
        result = [{
            'driver_id': driver.pk,
            'name': driver.name,
            'phone_number': driver.phone_number
        } for driver in car.driver.filter(is_active=True)]
        return result

from rest_framework import serializers
from .models import Site, Car
from django.core import validators


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

        def validate_name(self, attrs):
            validators.RegexValidator(r'^[가-힣a-zA-Z0-9\s]{1,50}$', '이름 형식이 맞지 않습니다.')(attrs)
            return attrs

        def validate_start_date(self, attrs):
            validators.RegexValidator(r'^(19|20)\d{2}-(0[1-9]|1[012])$', '날짜 형식이 맞지 않습니다.')(attrs)
            return attrs

        def validate_end_date(self, attrs):
            validators.RegexValidator(r'^(19|20)\d{2}-(0[1-9]|1[012])$', '날짜 형식이 맞지 않습니다.')(attrs)
            return attrs


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

    def validate_number(self, attrs):
        validators.RegexValidator(r'^[가-힣]{2}\d{2}[가-힣]{1}\d{4}$', '차량 번호 형식이 맞지 않습니다.')(attrs)
        return attrs

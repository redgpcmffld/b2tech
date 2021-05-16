from rest_framework import serializers
from .models import Driver, Admin
from django.core import validators


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

    def validate_name(self, attrs):
        validators.RegexValidator(r'^[가-힣]{2,}$|^[a-z]{2,}$', '이름은 2글자 이상 한글이거나 영어이어야 합니다.')(attrs)
        return attrs

    def validate_phone_number(self, attrs):
        validators.RegexValidator(r'^\d{11}$', 'invalid phone number format')(attrs)
        return attrs


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin
        fields = '__all__'

    def validate_account_name(self, attrs):
        validators.RegexValidator(r'^([a-z][A-Z]){2,}$', '계정이름은 2글자 이상 영문이어야 합니다.')(attrs)
        return attrs

    def validate_name(self, attrs):
        validators.RegexValidator(r'^[가-힣]{2,}$|^[a-z]{2,}$', '이름은 2글자 이상 한글이거나 영문이어야 합니다.')(attrs)
        return attrs

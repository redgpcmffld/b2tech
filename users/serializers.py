import bcrypt

from django.core import validators

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from projects.models import Site
from .models import Driver, Admin


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
        return attrs


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

    def validate_account_name(self, attrs):
        if Admin.objects.filter(account_name=attrs).exists():
            raise validators.ValidationError('이미 존재하는 아이디 입니다.')
        validators.RegexValidator(r'^\w{2,}$', '계정이름은 2글자 이상 영문,숫자이어야 합니다.')(attrs)
        return attrs

    def validate_name(self, attrs):
        validators.RegexValidator(r'^[가-힣]{2,}$|^[a-z]{2,}$', '이름은 2글자 이상 한글이거나 영문이어야 합니다.')(attrs)
        return attrs

    def validate_password(self, attrs):
        validators.RegexValidator(r'^(?=.*\w)(?=.*[!@#$%&*])(\S){8,}$',
                                  '비밀번호는 영문,숫자,특수문자 포함 8글자 이상이어야 합니다.')(attrs)
        attrs = bcrypt.hashpw(attrs.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return attrs

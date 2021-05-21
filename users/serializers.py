import bcrypt

from rest_framework.response import Response
from rest_framework import serializers
from django.core import validators

from .models import Admin

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

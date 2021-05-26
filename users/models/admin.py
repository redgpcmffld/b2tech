from django.db import models
from django.core import validators

import bcrypt
from rest_framework import serializers

from projects.models.project import Project
from projects.models.site import Site


class Admin(models.Model):
    TYPES = (('ProjectTotalAdmin', '프로젝트 전체 관리자'), ('SiteAdmin', '현장 관리자'))
    admin_id = models.BigAutoField(primary_key=True)
    account_name = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=TYPES)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    project = models.ManyToManyField(Project, related_name='project_admin', blank=True)
    site = models.ManyToManyField(Site, related_name='site_admin', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'admins'


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

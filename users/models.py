from django.db import models


class Admin(models.Model):
    TYPES = (('ProjectTotalAdmin', '프로젝트 전체 관리자'), ('SiteAdmin', '현장 관리자'))

    admin_id = models.AutoField(primary_key=True)
    account_name = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=TYPES)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'admins'


class Driver(models.Model):
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'drivers'
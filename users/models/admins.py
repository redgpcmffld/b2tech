from django.db import models

from projects.models.projects import Project
from projects.models.sites import Site


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

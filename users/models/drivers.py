from django.db import models

from projects.models.sites import Site


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

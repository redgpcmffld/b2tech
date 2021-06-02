from django.db import models

from projects.models.sites import Site


class Location(models.Model):
    from projects.models.resources import Resource
    location_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    site = models.ManyToManyField(Site)
    longitude = models.DecimalField(max_digits=15, decimal_places=12)
    latitude = models.DecimalField(max_digits=15, decimal_places=12)
    type = models.BooleanField()
    resource = models.ManyToManyField(Resource)
    plan = models.IntegerField()
    range = models.IntegerField()
    is_allow = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'locations'

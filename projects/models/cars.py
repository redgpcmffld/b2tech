from django.db import models

from projects.models.sites import Site
from users.models.drivers import Driver


class Car(models.Model):
    TYPES = (('DumpTruck', '덤프 트럭'), ('WasteTruck', '폐기물 트럭'), ('RecyclingTruck', '재활용 트럭'), ('Tank', '탱크'))

    car_id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=TYPES)
    number = models.CharField(max_length=20)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    driver = models.ManyToManyField(Driver, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'cars'

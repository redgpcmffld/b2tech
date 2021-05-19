from django.db import models


class Project(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'projects'


class Site(models.Model):
    site_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sites'


class Car(models.Model):
    TYPES = (('DumpTruck', '덤프 트럭'), ('WasteTruck', '폐기물 트럭'), ('RecyclingTruck', '재활용 트럭'), ('Tank', '탱크'))

    car_id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=TYPES)
    number = models.CharField(max_length=20)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    driver = models.ManyToManyField('users.Driver', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'cars'


class Resource(models.Model):
    TYPES = (('Ton', '톤'), ('Kg', '킬로그램'), ('m**3', '삼제곱미터'))

    resource_id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    block = models.CharField(max_length=10, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'resources'


class Location(models.Model):
    location_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    site = models.ManyToManyField(Site)
    longitude = models.DecimalField(max_digits=20, decimal_places=17)
    latitude = models.DecimalField(max_digits=20, decimal_places=17)
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

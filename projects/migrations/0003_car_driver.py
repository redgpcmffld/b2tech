# Generated by Django 3.2.2 on 2021-05-16 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210516_1715'),
        ('projects', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='driver',
            field=models.ManyToManyField(blank=True, to='users.Driver'),
        ),
    ]

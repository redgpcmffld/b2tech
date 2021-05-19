# Generated by Django 3.2.2 on 2021-05-19 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20210517_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='resource',
        ),
        migrations.AddField(
            model_name='location',
            name='resource',
            field=models.ManyToManyField(to='projects.Resource'),
        ),
    ]

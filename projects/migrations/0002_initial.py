# Generated by Django 3.2.2 on 2021-05-16 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='admin',
            field=models.ManyToManyField(blank=True, to='users.Admin'),
        ),
        migrations.AddField(
            model_name='site',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
        migrations.AddField(
            model_name='project',
            name='admin',
            field=models.ManyToManyField(blank=True, to='users.Admin'),
        ),
        migrations.AddField(
            model_name='location',
            name='resource',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.resource'),
        ),
        migrations.AddField(
            model_name='location',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.site'),
        ),
        migrations.AddField(
            model_name='car',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.site'),
        ),
    ]

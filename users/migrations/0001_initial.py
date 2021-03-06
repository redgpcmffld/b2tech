# Generated by Django 3.2.2 on 2021-05-21 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('driver_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.site')),
            ],
            options={
                'db_table': 'drivers',
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('account_name', models.CharField(max_length=20)),
                ('type', models.CharField(choices=[('ProjectTotalAdmin', '프로젝트 전체 관리자'), ('SiteAdmin', '현장 관리자')], max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('project', models.ManyToManyField(blank=True, related_name='project_admin', to='projects.Project')),
                ('site', models.ManyToManyField(blank=True, related_name='site_admin', to='projects.Site')),
            ],
            options={
                'db_table': 'admins',
            },
        ),
    ]

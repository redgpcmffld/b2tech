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
            name='DriveRecord',
            fields=[
                ('drive_record_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('transport_weight', models.IntegerField()),
                ('loading_time', models.DateTimeField()),
                ('unloading_time', models.DateTimeField(null=True)),
                ('driving_date', models.DateField()),
                ('total_distance', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('status', models.SmallIntegerField(choices=[(1, '상차'), (2, '정상종료'), (3, '강제하차승인요청'), (4, '강제하차확인')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.car')),
                ('loading_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loading_location', to='projects.location')),
                ('unloading_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unloading_location', to='projects.location')),
            ],
            options={
                'db_table': 'drive_records',
            },
        ),
        migrations.CreateModel(
            name='DriveRoute',
            fields=[
                ('drive_route_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('latitude', models.DecimalField(decimal_places=12, max_digits=15)),
                ('longitude', models.DecimalField(decimal_places=12, max_digits=15)),
                ('distance', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('drive_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.driverecord')),
            ],
            options={
                'db_table': 'drive_routes',
            },
        ),
    ]

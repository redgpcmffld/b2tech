# Generated by Django 3.2.2 on 2021-05-16 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriveRecord',
            fields=[
                ('drive_record_id', models.AutoField(primary_key=True, serialize=False)),
                ('transport_weight', models.IntegerField()),
                ('loading_time', models.DateTimeField()),
                ('unloading_time', models.DateTimeField()),
                ('driving_date', models.DateField()),
                ('total_distance', models.DecimalField(decimal_places=4, max_digits=10)),
                ('status', models.SmallIntegerField()),
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
    ]
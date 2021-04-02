# Generated by Django 3.1.7 on 2021-04-01 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertsCopy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=400, null=True)),
                ('warning_lower_copy', models.CharField(max_length=400, null=True)),
                ('warning_upper_copy', models.CharField(max_length=400, null=True)),
                ('alert_lower_copy', models.CharField(max_length=400, null=True)),
                ('alert_upper_copy', models.CharField(max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=70)),
                ('room', models.CharField(max_length=70)),
                ('device_id', models.CharField(max_length=70, unique=True)),
                ('airtable_plant_id', models.CharField(max_length=70)),
                ('current_temp', models.DecimalField(decimal_places=1, max_digits=4, null=True)),
                ('current_humidity', models.DecimalField(decimal_places=1, max_digits=4, null=True)),
                ('current_soilmoist', models.DecimalField(decimal_places=1, max_digits=4, null=True)),
                ('current_sun', models.IntegerField(null=True)),
                ('current_waterlevel_ok', models.BooleanField(null=True)),
                ('image_url', models.CharField(max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlantToleranceLimits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warning_lower', models.IntegerField(null=True)),
                ('warning_upper', models.IntegerField(null=True)),
                ('alert_lower', models.IntegerField(null=True)),
                ('alert_upper', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReadingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperatureF', models.DecimalField(decimal_places=1, max_digits=4, null=True)),
                ('humidity', models.DecimalField(decimal_places=1, max_digits=4, null=True)),
                ('soilmoist', models.DecimalField(decimal_places=1, max_digits=4, null=True)),
                ('sun', models.IntegerField(null=True)),
                ('valid_datetime', models.DateTimeField()),
                ('entry_id', models.CharField(max_length=70, null=True)),
                ('device_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plants.device')),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airtable_id', models.CharField(max_length=70, null=True)),
                ('scientific_name', models.CharField(max_length=170, null=True)),
                ('plant_name', models.CharField(max_length=70, null=True)),
                ('plant_type', models.CharField(max_length=70, null=True)),
                ('description', models.CharField(max_length=300, null=True)),
                ('ideal_soil_type', models.CharField(max_length=170, null=True)),
                ('toxicity', models.CharField(max_length=170, null=True)),
                ('containers', models.CharField(max_length=170, null=True)),
                ('water_preference', models.CharField(max_length=170, null=True)),
                ('sun_requirements', models.CharField(max_length=170, null=True)),
                ('underground_structures', models.CharField(max_length=170, null=True)),
                ('plant_uses', models.CharField(max_length=170, null=True)),
                ('small_thumbnail_url', models.CharField(max_length=170, null=True)),
                ('large_thumbnail_url', models.CharField(max_length=170, null=True)),
                ('humidity_limits', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='humidity_limits', to='plants.planttolerancelimits')),
                ('soilmoist_limits', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='soilmoist_limits', to='plants.planttolerancelimits')),
                ('sun_limits', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sun_limits', to='plants.planttolerancelimits')),
                ('temp_limits', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='temp_limits', to='plants.planttolerancelimits')),
            ],
        ),
        migrations.CreateModel(
            name='EventHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=400, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plants.device')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['updated_at'],
            },
        ),
        migrations.AddField(
            model_name='device',
            name='plant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plants.plant'),
        ),
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 3.1.6 on 2021-02-02 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0006_merge_20210201_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventhistory',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plants.device'),
        ),
    ]

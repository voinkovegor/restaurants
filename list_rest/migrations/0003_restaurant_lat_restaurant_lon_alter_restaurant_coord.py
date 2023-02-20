# Generated by Django 4.1.7 on 2023-02-20 04:24

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_rest', '0002_alter_restaurant_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='lat',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='lon',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='coord',
            field=django.contrib.gis.db.models.fields.PointField(dim=models.FloatField(), srid=4326, verbose_name=models.FloatField()),
        ),
    ]
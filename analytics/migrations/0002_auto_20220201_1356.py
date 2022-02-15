# Generated by Django 2.2.21 on 2022-02-01 13:56

from django.db import migrations
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeder_gis',
            name='pillar',
            field=djgeojson.fields.PolygonField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='feeder_gis',
            name='load',
            field=djgeojson.fields.PointField(blank=True, null=True),
        ),
    ]
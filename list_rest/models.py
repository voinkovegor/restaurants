from django.contrib.gis.db import models
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations

class Migration(migrations.Migration):

    operations = [
        CreateExtension('postgis'),
    ]


class Restaurant(models.Model):
    title = models.CharField(max_length=100)
    adress = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    #coord = models.PointField(lat, lon)

    def __str__(self):
        return self.title + ' ' + self.adress

    class Meta:
        ordering = ['title', 'adress']
        app_label = 'list_rest'

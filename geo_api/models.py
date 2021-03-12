from django.db import models


class IPGeoData(models.Model):
    ip = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    continent_code = models.CharField(max_length=200)
    continent_name = models.CharField(max_length=200)
    country_code = models.CharField(max_length=200)
    country_name = models.CharField(max_length=200)
    region_code = models.CharField(max_length=200)
    region_name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zip = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()

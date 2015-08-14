# coding=utf-8

from django.db import models

from django_earthdistance.models import EarthDistanceQuerySet

class TestModel(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

    objects = EarthDistanceQuerySet.as_manager()


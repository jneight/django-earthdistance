# coding=utf-8

from django.db import models

from django_earthdistance.models import EarthDistanceQuerySet

class TestModel(models.Model):
    c_lat = models.FloatField()
    c_lon = models.FloatField()

    objects = EarthDistanceQuerySet.as_manager()


class RelatedTestModel(models.Model):
    related = models.ForeignKey(
        TestModel,
        on_delete=models.CASCADE
    )

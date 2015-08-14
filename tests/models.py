# coding=utf-8

from django.db import models


class TestModel(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()



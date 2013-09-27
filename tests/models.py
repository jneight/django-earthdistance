# coding=utf-8

from django.db import models
from djorm_expressions.models import ExpressionManager


class TestModel(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

    objects = ExpressionManager()


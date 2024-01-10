# coding=utf-8
from django.db import models
from django.db.models import Func


class LlToEarth(Func):
    function = 'll_to_earth'

    def __init__(self, params, output_field=None):
        if output_field is None:
            output_field = models.fields.Field()
        self.params = params
        super(LlToEarth, self).__init__(*params, output_field=output_field)


class EarthDistance(Func):
    function = 'earth_distance'

    def __init__(self, expressions, output_field=None):
        if output_field is None:
            output_field = models.fields.Field()
        self.expressions = expressions
        super(EarthDistance, self).__init__(*expressions, output_field=output_field)


class EarthDistanceQuerySet(models.QuerySet):
    def in_distance(self, distance, fields, points, annotate='_ed_distance'):
        """Filter rows inside a circunference of radius distance `distance`

            :param distance: max distance to allow
            :param fields: `tuple` with the fields to filter (latitude, longitude)
            :param points: center of the circunference (latitude, longitude)
            :param annotate: name where the distance will be annotated

        """
        clone = self._clone()
        return clone.annotate(
            **{annotate: EarthDistance([
                LlToEarth(fields), LlToEarth(points)])
            }).filter(**{'{0}__lte'.format(annotate): distance})


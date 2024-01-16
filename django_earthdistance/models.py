# coding=utf-8

from django.db import models


class LlToEarth(models.Func):
    """
    Returns the location of a point on the surface of the Earth given its
    latitude and longitude in degrees.
    """
    function = "ll_to_earth"
    arg_joiner = ", "
    arity = 1


class EarthDistance(models.Func):
    """
    This PostgreSQL function returns the great circle distance between two points on the surface of the
    earth.
    """
    template = 'earth_distance(%(expressions)s)'

    def __init__(self, expressions, output_field=None):
        if output_field is None:
            output_field = models.fields.Field()
        self.expressions = expressions
        super(EarthDistance, self).__init__(output_field=output_field)

    def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False):
        """Prepare SQL from inner funcions (ll_to_earth or any other)"""
        c = self.copy()
        c.is_summary = summarize
        c.for_save = for_save
        for pos, expression in enumerate(self.expressions):
            c.expressions[pos] = expression.resolve_expression(query, allow_joins, reuse, summarize)
        return c

    def as_sql(self, compiler, connection):
        sql_expressions, sql_params = [], []

        for expression in self.expressions:
            sql, params = compiler.compile(expression)
            sql_expressions.append(sql)
            sql_params.extend(params)
        return self.template % {'expressions': ','.join(sql_expressions)}, sql_params


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


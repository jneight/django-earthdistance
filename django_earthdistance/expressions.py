# coding=utf-8

from djorm_expressions.base import SqlExpression, SqlNode

from .functions import LlToEarth, EarthBox


class EarthDistanceExpression(SqlExpression):
    sql_template = "%(field)s %(operator)s %(value)s"

    def __init__(self, field_or_func, operator, value=None, **kwargs):
        self.operator = operator
        self.extra = kwargs

        if isinstance(field_or_func, SqlNode):
            self.sql_function = field_or_func
        else:
            self.sql_function = None

        if isinstance(value, SqlNode):
            self.value_function = value
        else:
            self.value_function = None

    def as_sql(self, qn, queryset):
        args = []
        function_sql, _args = self.sql_function.as_sql(qn, queryset)
        if _args:
            args.extend(_args)
        if self.value_function:
            value_sql, _args = self.value_function.as_sql(qn, queryset)
            if _args:
                args.append(_args)

        template_result = self.sql_template % {
            'field': function_sql,
            'operator': self.operator,
            'value': value_sql
        }
        if self.negated:
            return self.sql_negated_template % (template_result), args
        return template_result, args


class DistanceExpression(object):
    def __init__(self, fields):
        self.fields = fields

    def in_distance(self, distance, points):
        """
            Builds a query using earth_box and ll_to_earth

            SELECT * FROM "venues_venue" WHERE
                earth_box(ll_to_earth(12.23,15.25),10000) @> ll_to_earth(lat,lon)
        """
        return EarthDistanceExpression(
            EarthBox(LlToEarth(points), distance), '@>', LlToEarth(self.fields))






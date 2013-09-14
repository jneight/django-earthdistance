# coding=utf-8

from djorm_expressions.base import SqlFunction
from djorm_expressions.utils import _setup_joins_for_fields

from .utils import is_sequence


class LlToEarth(SqlFunction):
    """
        This function builds a point in the earth surface using two floats
    """
    sql_function = u'll_to_earth'
    sql_template = u'%(function)s(%(x)s,%(y)s)'

    def __init__(self, points, *args, **kwargs):
        if not is_sequence(points):
            raise TypeError('points attr need to be a list')
        self.points = points
        self.field = None
        self.args = args
        self.extern_params = kwargs

    def as_sql(self, qn, queryset):
        """
            Returns final sql expression:
                ll_to_earth(column1, column2)

            JOIN is supported
        """
        try:
            # columns with '__' are joins
            for i, p in enumerate(self.points):
                _setup_joins_for_fields(p.split('__'), self, queryset)
                _tbl, _fld, _alias = self.field
                if _tbl == _alias:
                    self.points[i] = "%s.%s" % (qn(_tbl), qn(_fld))
                else:
                    self.points[i] = "%s.%s" % (_alias, qn(_fld))
        except AttributeError:
            pass
        return self.sql_template % {
            'function': self.sql_function,
            'x': self.points[0],
            'y': self.points[1]}, self.args


class CubeDistance(SqlFunction):
    sql_function = 'cube_distance'
    sql_template = '%(function)s(%(points)s,%(fields)s)'

    def __init__(self, points_function, fields_function, *args, **kwargs):
        self.points_function = points_function
        self.fields_function = fields_function
        self.args = args
        self.extern_params = kwargs

    def as_sql(self, qn, queryset):
        """
            Returns final sql expression:
                earth_box(ll_to_earth(column1, column2), distance)
        """
        final_args = []
        final_args.extend(self.args,)
        points_sql, _args = self.points_function.as_sql(qn, queryset)
        final_args.extend(_args)
        fields_sql, _args = self.fields_function.as_sql(qn, queryset)
        final_args.extend(_args)
        return self.sql_template % {
            'function': self.sql_function,
            'points': points_sql,
            'fields': fields_sql,
        }, final_args


class EarthBox(SqlFunction):
    """
        This function build a box around one point using distance
    """
    sql_function = 'earth_box'
    sql_template = '%(function)s(%(inside)s,%(distance)s)'

    def __init__(self, inside_function, distance, *args, **kwargs):
        self.inside_function = inside_function
        self.distance = distance
        self.args = args
        self.extern_params = kwargs

    def as_sql(self, qn, queryset):
        """
            Returns final sql expression:
                earth_box(ll_to_earth(column1, column2), distance)
        """
        final_args = []
        inside_sql, _args = self.inside_function.as_sql(qn, queryset)
        final_args.extend(self.args,)
        final_args.extend(_args)
        return self.sql_template % {
            'function': self.sql_function,
            'inside': inside_sql,
            'distance': self.distance
        }, []

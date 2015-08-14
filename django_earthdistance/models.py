# coding=utf-8

import copy
import six

from django.db.models import fields
from django.db.models.expressions import RawSQL
from django.db.models import Expression

class LlToEarth(Expression):
    template = 'll_to_earth(%(params)s)'

    def __init__(self, params, output_field=None):
        if output_field is None:
            output_field = fields.Field()
        self.params = params
        super(LlToEarth, self).__init__(output_field=output_field)

    def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False):
        """Setup any data here, this method will be called before final SQL is generated"""
        c = self.copy()
        c.is_summary = summarize
        c.for_save = for_save
        final_points = []
        for i, p in enumerate(self.params):
            try:
                float(p)
            except:
                _, source, _, join_list, last = query.setup_joins(
                    six.text_type(p).split('__'), query.model._meta, query.get_initial_alias())
                target, alias, _ = query.trim_joins(source, join_list, last)
                final_points.append("%s.%s" % (alias, target[0].get_attname_column()[1]))
            else:
                final_points.append(six.text_type(p))
            c.params = final_points
        return c

    def as_sql(self, compiler, connection):
        """Returns ll_to_earth(field,field)"""
        return self.template % {'params': ','.join(self.params)}, []


class CubeDistance(Expression):
    template = 'cube_distance(%(expressions)s)'

    def __init__(self, expressions, output_field=None):
        if output_field is None:
            output_field = fields.Field()
        self.expressions = expressions
        super(CubeDistance, self).__init__(output_field=output_field)

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


# coding=utf-8

import decimal
import collections

from django.utils.six import with_metaclass
from django.db import models


class LatLongFieldProxy(object):
    def __init__(self, owner, latitude_field, longitude_field):
        self._owner = owner
        self._latitude_field = latitude_field
        self._longitude_field = longitude_field

    @property
    def lat(self):
        return getattr(self._owner, self._latitude_field)

    @lat.setter
    def lat(self, value):
        setattr(self._owner, self._latitude_field, value)

    @property
    def lon(self):
        return getattr(self._owner, self._longitude_field)

    @lon.setter
    def lon(self, value):
        setattr(self._owner, self._longitude_field, value)

    def __str__(self):
        return u'Point(lat: {0}, lon: {1})'.format(self.lat, self.lon)


class LatLongDescriptor(object):
    def __init__(self, latitude_field, longitude_field, **kwargs):
        self.latitude_field = latitude_field
        self.longitude_field = longitude_field

    def __get__(self, obj, owner=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        return LatLongFieldProxy(
            owner=obj, latitude_field=self.latitude_field,
            longitude_field=self.longitude_field)

    def __set__(self, instance, value):
        setattr(instance, self.latitude_field, value.lat)
        setattr(instance, self.longitude_field, value.lon)

    #def contribute_to_class(self, cls, name, **kwargs):
        # dynamic field creation is not recommended for django 1.7
        #name_lat = '{0}_{1}'.format(name, self.name_lat_base)
        #field_lat = models.FloatField()
        #field_lat.creation_counter = self.creation_counter
        #cls.add_to_class(name_lat, field_lat)

        #name_lon = '{0}_{1}'.format(name, self.name_lon_base)
        #field_lon = models.FloatField()
        #field_lon.creation_counter = self.creation_counter
        #cls.add_to_class(name_lon, field_lon)

        #super(LatLongField, self).contribute_to_class(cls, name, **kwargs)
        #setattr(cls, name_lat, field_lat)
        #setattr(cls, name_lon, field_lon)



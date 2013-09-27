# coding=utf-8

from django.test import TestCase

from django_earthdistance.expressions import DistanceExpression
from django_earthdistance.functions import CubeDistance, LlToEarth

from .models import TestModel


class EarthdistanceTest(TestCase):
    def setUp(self):
        self.obj_1 = TestModel.objects.create(lat=51.490857, lon=-0.15071)
        self.obj_2 = TestModel.objects.create(lat=39.74829, lon=-1.23854)
        self.obj_3 = TestModel.objects.create(lat=39.46487, lon=-1.23854)

    def test_in_distance(self):
        objects = TestModel.objects.where(
            DistanceExpression(['lat', 'lon']).in_distance(
                1500, (float(51.490857), float(-0.15071))))
        self.assertEqual(objects.count(), 1)
        self.assertEqual(objects[0].pk, self.obj_1.pk)

        objects = TestModel.objects.where(
            DistanceExpression(['lat', 'lon']).in_distance(
                100000, (float(39.49087), float(-1.15071))))
        self.assertEqual(objects.count(), 2)
        self.assertTrue(
            all(o.pk in [self.obj_2.pk, self.obj_3.pk] for o in objects))

    def test_annotate(self):
        objects = TestModel.objects.where(
            DistanceExpression(['lat', 'lon']).in_distance(
                10000, (float(39.49087), float(-1.15071)))).annotate_functions(
                distance=CubeDistance(
                    LlToEarth([float(39.49087), float(-1.15071)]),
                    LlToEarth(['lat', 'lon'])))
        self.assertEqual(objects.count(), 1)
        self.assertEqual(int(objects[0].distance), 8082)


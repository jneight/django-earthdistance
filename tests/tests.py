# coding=utf-8

from django.test import TestCase

from django_earthdistance.models import EarthDistance, LlToEarth

from .models import TestModel


class EarthdistanceTest(TestCase):
    def setUp(self):
        self.obj_1 = TestModel.objects.create(lat=51.490857, lon=-0.15071)
        self.obj_2 = TestModel.objects.create(lat=39.74829, lon=-1.23854)
        self.obj_3 = TestModel.objects.create(lat=39.46487, lon=-1.23854)

    def test_in_distance(self):
        objects = TestModel.objects.in_distance(
            1500, ('lat', 'lon'), (float(51.490857), float(-0.15071)))
        self.assertEqual(objects.count(), 1)
        self.assertEqual(objects[0].pk, self.obj_1.pk)
        self.assertTrue(hasattr(objects[0], '_ed_distance'))
        objects = TestModel.objects.in_distance(
            100000, ('lat', 'lon'), (float(39.49087), float(-1.15071)))
        self.assertEqual(objects.count(), 2)
        self.assertTrue(
            all(o.pk in [self.obj_2.pk, self.obj_3.pk] for o in objects))

    def test_annotate(self):
        obj = TestModel.objects.annotate(
            distance=EarthDistance([
                LlToEarth(('lat', 'lon')),
                LlToEarth((float(39.49087), float(-1.15071)))
            ])).get(id=self.obj_1.id)
        self.assertEqual(int(obj.distance), 1338082)


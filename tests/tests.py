# coding=utf-8

from django.test import TestCase
from django.db.models import Case, When, Value, BooleanField, Q
from django_earthdistance.models import EarthDistance, LlToEarth

from .models import TestModel, RelatedTestModel


class EarthdistanceTest(TestCase):
    def setUp(self):
        self.obj_1 = TestModel.objects.create(c_lat=51.490857, c_lon=-0.15071)
        self.obj_2 = TestModel.objects.create(c_lat=39.74829, c_lon=-1.23854)
        self.obj_3 = TestModel.objects.create(c_lat=39.46487, c_lon=-1.23854)
        self.obj_related = RelatedTestModel.objects.create(related=self.obj_1)

    def test_in_distance(self):
        objects = TestModel.objects.in_distance(
            1500, ('c_lat', 'c_lon'), (float(51.490857), float(-0.15071)))
        self.assertEqual(objects.count(), 1)
        self.assertEqual(objects[0].pk, self.obj_1.pk)
        self.assertTrue(hasattr(objects[0], '_ed_distance'))
        objects = TestModel.objects.in_distance(
            100000, ('c_lat', 'c_lon'), (float(39.49087), float(-1.15071)))
        self.assertEqual(objects.count(), 2)
        self.assertTrue(
            all(o.pk in [self.obj_2.pk, self.obj_3.pk] for o in objects))

    def test_annotate(self):
        obj = TestModel.objects.annotate(
            distance=EarthDistance([
                LlToEarth(('c_lat', 'c_lon')),
                LlToEarth((float(39.49087), float(-1.15071)))
            ])).get(id=self.obj_1.id)
        self.assertEqual(int(obj.distance), 1338082)

    def test_annotate_with_join(self):
        obj = RelatedTestModel.objects.annotate(
            distance=EarthDistance([
                LlToEarth((39.49087, -1.15071)),
                LlToEarth(('related__c_lat', 'related__c_lon'))
            ])
        ).annotate(
            inradius=Case(
                When(Q(distance__lte=2.0), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).first()
        self.assertEqual(int(obj.distance), 1338082)
        self.assertFalse(obj.inradius)

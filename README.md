django-earthdistance
====================

Using PostgreSQL's EarthDistance extension with django and django-ext-*

Usage
---------------

Cube and EarthDistance extensions must be enabled in postgreSQL BD, so logs in
database using pgsql and install extensions:

```
=> create extension cube;
=> create extension earthdistance;
```

Extension is built using `djorm-ext-core <https://github.com/niwibe/djorm-ext-core>`
and `djorm-ext-expressions <https://github.com/niwibe/djorm-ext-expressions>` packages.

### Filter by rows inside a circle of distance radious ###

```python
from django_earthdistance.expressions import DistanceExpression
from django_earthdistance.functions import CubeDistance, LlToEarth
from djorm_expressions.models import ExpressionManager

class MyModel(models.Model):
    latitute = models.FloatField()
    longitude = models.FloatField()

    objects = ExpressionManager()

# Define fields to query in DistanceExpression initialization
# search with lat=0.2546 and lon=-38.25 and distance 1500 meters

MyModel.objects.where(
    DistanceExpression(['latitude', 'longitude']).in_distance(
        1500,
        [0.2546, -38.25]))
```
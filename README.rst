django-earthdistance
=====================

Using PostgreSQL's EarthDistance extension for django >= 1.8 (for older versions see *with_djorm_expressions* branch)

Earthdistance allows to do fast geolocalized queries without using PostGIS

**Tested with python 2.7 and 3.3**


Usage
---------------

Cube and EarthDistance extensions must be enabled in postgreSQL BD, so log in
database using pgsql and install extensions:

.. code:: sql

    => create extension cube;
    => create extension earthdistance;



Filter by rows inside a circunference of radius r
--------------------------------------------------

.. code:: python

    from django.db import models

    from django_earthdistance.models import EarthDistanceQuerySet

    class MyModel(models.Model):
        latitute = models.FloatField()
        longitude = models.FloatField()

        objects = EarthDistanceQuerySet.as_manager()

    # Define fields to query in DistanceExpression initialization
    # search with lat=0.2546 and lon=-38.25 and distance 1500 meters
    # use param `annotate` to set a custom field for the distance, `_ed_distance` as default

    MyModel.objects.in_distance(1500, fields=['latitude', 'longitude'], points=[0.2546, -38.25])


Annotate each row returned by a query with distance between two points
----------------------------------------------------------------------

.. code:: python

    from django_earthdistance.models import EarthDistance, LlToEarth

    MyModel.objects.filter(....).annotate(
        distance=EarthDistance([
            LlToEarth([0.2546, -38.25]),
            LlToEarth(['latitude', 'longitude'])
        ]))



Optimizing perfomance with indexes
-----------------------------------

PostgreSQL allow to use GiST indexes with functions results, a good perfomance improvement is to store `ll_to_earth` results in
an index, `ll_to_earth` is a function that calculates the position of a point on the surface of the earth (assuming earth is 
perfectly spherical)


.. code:: sql
   
    -- Example MyModel table is app_mymodel and points columns are latitude and longitude
    CREATE INDEX mymodel_location ON app_mymodel USING gist (ll_to_earth(latitude, longitude));

For django < 1.7
~~~~~~~~~~~~~~~~~

Also, using south is preferred, just add this migration to migrations/ folder and edit it to your needs, index will be created

.. code:: python

    class Migration(SchemaMigration):

        def forwards(self, orm):
            cursor = connection.cursor()
            cursor.execute("CREATE INDEX mymodel_location ON app_mymodel USING gist (ll_to_earth(latitude, longitude));")


        def backwards(self, orm):
            # Deleting field 'Venue.coords'
            cursor = connection.cursor()
            cursor.execute("DROP INDEX mymodel_location ON app_mymodel;")


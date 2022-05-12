#!/usr/bin/env python
import sys
import os

import django
from django.conf import settings
from django.test.runner import DiscoverRunner


settings.configure(
    DEBUG=True,
    DATABASES={
        'default':{
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'test',
            'USER': os.environ['POSTGRES_USER'],
            'PASSWORD': os.environ['PGPASSWORD'],
            'HOST': 'localhost',
        }
    },
    INSTALLED_APPS=(
        'django_earthdistance',
        'tests',
    ),
    USE_TZ=True,
)

django.setup()
test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests(['tests', ])
if failures:
    sys.exit(failures)

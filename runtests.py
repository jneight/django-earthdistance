#!/usr/bin/env python
import sys

import django
from django.conf import settings


settings.configure(
    DEBUG=True,
    DATABASES={
        'default':{
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'test',
            'USER': 'postgres',
            'PASSWORD': 'postgres', }
    },
    INSTALLED_APPS=(
        'django_earthdistance',
        'tests',
    ),
    USE_TZ=True,
)

try:
    django.setup()
except AttributeError:
    pass # not using django 1.7 or newer

try:
    from django.test.runner import DiscoverRunner as TestSuiteRunner
except ImportError:  # DiscoverRunner is the preferred one for django > 1.7
    from django.test.simple import DjangoTestSuiteRunner as TestSuiteRunner


test_runner = TestSuiteRunner(verbosity=1)

failures = test_runner.run_tests(['tests', ])
if failures:
    sys.exit(failures)

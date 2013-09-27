#!/usr/bin/env python
import sys
from django.conf import settings


settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'test',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'OPTIONS': {'autocommit': True},
        }
    },
    INSTALLED_APPS=(
        'django_earthdistance',
        'tests',
    ),
    USE_TZ=True,
)

from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)

failures = test_runner.run_tests(['tests', ])
if failures:
    sys.exit(failures)

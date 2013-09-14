# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='django-earthdistance',
    version='0.3',
    install_requires=[
        'djorm-ext-core>=0.4.3',
        'djorm-ext-expressions>=0.5'],
    url='https://github.com/jneight/django-earthdistance',
    description='Add support for earthdistance PostgreSQL extension to Django',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    author='Javier Cordero Martinez',
    author_email='jcorderomartinez@gmail.com'
)

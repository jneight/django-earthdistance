# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='django-earthdistance',
    version='1.1.2',
    install_requires=[
        'django>=1.8'],
    url='https://github.com/jneight/django-earthdistance',
    description='Add support for PostgreSQL earthdistance extension to Django',
    long_description=open("README.rst").read(),
    packages=find_packages(),
    include_package_data=True,
    license='Apache 2.0',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    author='Javier Cordero Martinez',
    author_email='jcorderomartinez@gmail.com'
)

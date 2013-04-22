# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='django-earthdistance',
    version='0.1a',
    install_requires=[
        'djorm-ext-core==0.4.1',
        'djorm-ext-hstore==0.4.3',
        'djorm-ext-expressions==0.4.3'],
    url='https://github.com/jneight/django-earthdistance',
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
    author='Javier Cordero',
    author_email='jcorderomartinez@gmail.com'
)
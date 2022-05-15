# coding=utf-8
import codecs

from setuptools import setup, find_packages


def long_description():
    try:
        with codecs.open('README.md', 'r', 'utf-8') as f:
            return f.read()
    except:
        return 'Error loading README.md'


setup(
    name='django-earthdistance',
    version='1.1.3',
    install_requires=[
        'django>=1.8'],
    url='https://github.com/jneight/django-earthdistance',
    description='Add support for PostgreSQL earthdistance extension to Django',
    long_description=long_description(),
    long_description_content_type='text/markdown',
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
    author_email='github@j2i.me'
)

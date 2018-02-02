#!/usr/bin/env python
# encoding utf-8

import os
import re
from setuptools import setup, find_packages
import sys


main_py = open(os.path.join('kaio', '__init__.py')).read()
metadata = dict(re.findall("__([A-Z]+)__ = '([^']+)'", main_py))
__VERSION__ = metadata['VERSION']


install_requires = [
    'clint',
    'django-configurations>=2,<3',
]
if sys.version_info[0] < 3:
    install_requires.append('configparser')


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


setup(
    name='django-kaio',
    version=__VERSION__,
    author='APSL',
    author_email='engineering@apsl.net',
    url='https://github.com/APSL/django-kaio',
    packages=find_packages(),
    license='BSD',
    description="Class based settings for Django projects that can be read from multiple sources",
    long_description=README,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Internet :: WWW/HTTP',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
    ],
    include_package_data=True,
    zip_safe=False,
)

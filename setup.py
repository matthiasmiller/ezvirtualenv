#!/usr/bin/env python
# vim: sw=4 ts=4 et
from setuptools import setup

setup(name='ezvirtualenv',
      version='0.1.0',
      description='Easy Virtual Environment',
      author='Matthias Miller',
      url='https://github.com/matthiasmiller/ezvirtualenv',
      py_modules=['ezvirtualenv'],
      install_requires=[
        'virtualenv>=13.0.03',
      ],
     )


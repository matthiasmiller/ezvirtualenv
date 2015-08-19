#!/usr/bin/env python
# vim: sw=4 ts=4 et
from setuptools import setup

import ezvirtualenv

setup(
    name='ezvirtualenv',
    version=ezvirtualenv.__version__,
    description='Easy Virtual Environment',
    author='Matthias Miller',
    author_email='matthiasmiller@users.sf.net',
    url='https://github.com/matthiasmiller/ezvirtualenv',
    install_requires=[
        'virtualenv>=13.0.03',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    packages=['ezvirtualenv'],
)



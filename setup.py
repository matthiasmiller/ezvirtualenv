#!/usr/bin/env python
# vim: sw=4 ts=4 et
import os.path
import re
import sys
from setuptools import setup

def getversion():
    dir_ = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir_, 'ezvirtualenv', '__init__.py')) as f:
        match = re.search(r"__version__ = '([\d\.]+)'", f.read())
        assert match, 'Could not locate version!'
        return match.group(1)

install_requires = []
if sys.version_info < (3,):
    install_requires.append('virtualenv>=13.0.03')

setup(
    name='ezvirtualenv',
    version=getversion(),
    description='Easy Virtual Environment',
    author='Matthias Miller',
    author_email='matthiasmiller@users.sf.net',
    url='https://github.com/matthiasmiller/ezvirtualenv',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    packages=['ezvirtualenv'],
    zip_safe=False
)



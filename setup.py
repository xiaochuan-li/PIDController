#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
from pidcontroller import __version__
setup(
    name='PIDController',
    version=__version__,
    author='xiaochuan',
    url='https://github.com/xiaochuan-li/PIDController',
    author_email='lixiaochuan822@gmail.com',
    description=u'PIDController',
    packages=['pidcontroller'],
    install_requires=['matplotlib', 'numpy'],
    entry_points={
        'console_scripts': [
            'sayit=pidcontroller:sayit',
        ]
    }
)
#!/usr/bin/env python

import os
from setuptools import setup, find_packages


setup(
    name='emrichen',
    version='0.0.1',
    description='YAML preprocessor',
    long_description='',
    license='MIT',
    author='Santtu Pajukanta',
    author_email='santtu@pajukanta.fi',
    url='http://github.com/japsu/emrichen',
    packages = ['emrichen'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'emrichen = emrichen.__main__:main',
        ]
    },
    install_requires=["PyYAML", "pyaml"],
    tests_require=["pytest"],
    setup_requires=["pytest-runner"],
)

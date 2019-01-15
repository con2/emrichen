#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='emrichen',
    version='0.1.0',
    description='Template engine for YAML & JSON',
    long_description='',
    license='MIT',
    author='Santtu Pajukanta',
    author_email='santtu@pajukanta.fi',
    url='http://github.com/japsu/emrichen',
    packages = find_packages(exclude=["tests"]),
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'emrichen = emrichen.__main__:main',
        ]
    },
    install_requires=["PyYAML", "pyaml", "jsonpath-rw~=1.4.0"],
    tests_require=["pytest"],
    setup_requires=["pytest-runner"],
)

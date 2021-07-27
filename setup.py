#!/usr/bin/env python

import os
import re

from setuptools import find_packages, setup

source_dir = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(source_dir, 'emrichen', '__init__.py')) as f:
    init_file = f.read()
    match = re.search("__version__ = ['\"]([^'\"]+)['\"]", init_file)
    assert match, "Failed to parse version from emrichen/__init__.py"
    version = match.group(1)


with open(os.path.join(source_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

test_requirements = [
    "pytest~=6.2.3",
    "pytest-cov==2.11.1",
]

lint_requirements = [
    "black>=21.7b0",
    "flake8>=3.9.2",
    "mypy>=0.910",
    "isort>=5.9.2",
]

setup(
    name='emrichen',
    version=version,
    description='Template engine for YAML & JSON',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Santtu Pajukanta',
    author_email='santtu@pajukanta.fi',
    url='http://github.com/con2/emrichen',
    packages=find_packages(exclude=["tests"]),
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'emrichen = emrichen.__main__:main',
        ]
    },
    python_requires='>=3.6',
    install_requires=["PyYAML", "pyaml", "jsonpath-rw~=1.4.0"],
    extras_require={"test": test_requirements, "lint": lint_requirements},
)

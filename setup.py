#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='epitech_api',
    version='0.0',
    description='Epitech\'s API access for Python',
    author='KokaKiwi',
    author_email='kokakiwi@kokakiwi.net',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages(),
    install_requires=[
        'arrow',                # For better date handling
        'requests',             # For HTTP requests
    ],
)

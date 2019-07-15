#!/usr/bin/env python
# setup.py
# -*- coding: utf-8 -*-
# vim: ai et ts=4 sw=4 sts=4 fenc=UTF-8 ft=python

from setuptools import setup


with open('README.rst') as readme_file:
    README = readme_file.read()

with open('HISTORY.rst') as history_file:
    HISTORY = history_file.read()

REQUIREMENTS = [
    'boto',
    'requests',
]

TEST_REQUIREMENTS = [
    'pytest>=3.0.3',
    'pytest-cov>=2.4.0',
    'responses>=0.5.1',
    'tox>=2.4.1',
]

setup(
    name='clustercron',
    version='0.4.10',
    description='Cron job wrapper that ensures a script gets run from one node'
    ' in the cluster.',
    long_description=README + '\n\n' + HISTORY,
    author='Maarten Diemel',
    author_email='maarten@maartendiemel.nl',
    url='https://github.com/maartenq/clustercron',
    packages=[
        'clustercron',
    ],
    package_dir={'clustercron': 'clustercron'},
    entry_points={
        'console_scripts': [
            'clustercron = clustercron.main:main',
        ]
    },
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license="ISC license",
    zip_safe=False,
    keywords='clustercron',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Utilities',
    ],
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
)

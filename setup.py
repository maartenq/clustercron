#!/usr/bin/env python
# setup.py
# -*- coding: utf-8 -*-
# vim: ai et ts=4 sw=4 sts=4 fenc=UTF-8 ft=python

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        # Import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'boto==2.42.0',
    'requests==2.11.1',
]

test_requirements = [
    'pytest==3.0.0',
    'pytest-cov==2.3.1',
    'responses==0.5.1',
    'tox==2.3.1',
]

setup(
    name='clustercron',
    version='0.4.8',
    description='Cron job wrapper that ensures a script gets run from one node'
    ' in the cluster.',
    long_description=readme + '\n\n' + history,
    author='Maarten Diemel',
    author_email='maarten@maartendiemel.nl',
    url='https://github.com/maartenq/clustercron',
    packages=[
        'clustercron',
    ],
    package_dir={'clustercron': 'clustercron'},
    entry_points={
        'console_scripts': [
            'clustercron = clustercron.main:command',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license='BSD',
    zip_safe=False,
    keywords='clustercron',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Utilities',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
)

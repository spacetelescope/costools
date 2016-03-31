#!/usr/bin/env python
import relic.release
from glob import glob
from setuptools import setup, find_packages, Extension


version = relic.release.get_info()
relic.release.write_template(version, 'lib/costools')

setup(
    name = 'costools',
    version = version.pep386,
    author = 'Warren Hack, Nadezhda Dencheva, Phil Hodge',
    author_email = 'help@stsci.edu',
    description = 'Tools for COS (Cosmic Origins Spectrograph)',
    url = 'https://github.com/spacetelescope/costools',
    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires = [
        'astropy',
        'nose',
        'numpy',
        'sphinx',
        'stsci.tools'
    ],

    package_dir = {
        '':'lib'
    },
    packages = find_packages('lib'),
    package_data = {
        'costools': [
            'pars/*',
            '*.help',
        ]
    },
    entry_points = {
        'console_scripts': [
            'timefilter=costools.timefilter:main',
        ],
    },
)

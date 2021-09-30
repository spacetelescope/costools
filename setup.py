#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup


PACKAGENAME = 'costools'

setup(
    name=PACKAGENAME,
    use_scm_version={'write_to': 'costools/version.py'},
    setup_requires=['setuptools_scm'],
    install_requires=[
        'astropy',
        'calcos',
        'numpy',
        'stsci.tools',
    ],
    extras_require={
        'docs': [
            'sphinx',
            'numpydoc',
        ],
        'test': [
            'pytest',
            'pytest-cov',
            'codecov',
        ],
    },
    packages=find_packages(),
    package_data={
        PACKAGENAME: [
            'pars/*',
            '*.help',
        ],
    },
    entry_points={
        'console_scripts': [
            'timefilter = {0}.timefilter:main'.format(PACKAGENAME),
        ],
    },
    author='Warren Hack, Nadezhda Dencheva, Phil Hodge',
    author_email='help@stsci.edu',
    description='Tools for COS (Cosmic Origins Spectrograph)',
    url='https://github.com/spacetelescope/costools',
    license='BSD',
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

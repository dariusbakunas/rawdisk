#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
    'hexdump == 2.0',
    'yapsy == 1.10.323',
    'pyxdg == 0.25',
]

test_requirements = [
    # TODO: put package test requirements here
    'nose>=1.0',
    'mock==1.0.1',
]

setup(
    name='rawdisk',
    version='0.1.2',
    description='Experimental python code to explore different volume formats',
    long_description=readme + '\n\n' + history,
    author='Darius Bakunas-Milanowski',
    author_email='bakunas@gmail.com',
    url='https://github.com/dariusbakunas/rawdisk',
    packages=[
        'rawdisk',
        'rawdisk.filesystems',
        'rawdisk.plugins',
        'rawdisk.plugins.filesystems',
        'rawdisk.plugins.filesystems.apple_boot',
        'rawdisk.plugins.filesystems.efi_system',
        'rawdisk.plugins.filesystems.hfs_plus',
        'rawdisk.plugins.filesystems.ntfs',
        'rawdisk.scheme',
        'rawdisk.util',
    ],
    package_dir={'rawdisk':
                 'rawdisk'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='rawdisk',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts':[
            'rawdisk = rawdisk.main:main',
        ]
    }
)

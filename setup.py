# -*- coding: utf-8 -*-
import os
import sys
import imp
from setuptools import setup, find_packages

# Add the current directory to the module search path.
sys.path.append('.')

## Constants
CODE_DIRECTORY = 'rawdisk'
DOCS_DIRECTORY = 'docs'
TESTS_DIRECTORY = 'tests'


# Import metadata. Normally this would just be:
#
#     from $package import metadata
#
# However, when we do this, we also import `$package/__init__.py'. If this
# imports names from some other modules and these modules have third-party
# dependencies that need installing (which happens after this file is run), the
# script will crash. What we do instead is to load the metadata module by path
# instead, effectively side-stepping the dependency problem. Please make sure
# metadata has no dependencies, otherwise they will need to be added to
# the setup_requires keyword.
metadata = imp.load_source(
    'metadata', os.path.join(CODE_DIRECTORY, 'metadata.py'))

def read(filename):
    """Return the contents of a file.

    :param filename: file path
    :type filename: :class:`str`
    :return: the file's content
    :rtype: :class:`str`
    """
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()

setup(
    include_package_data = True,
    name=metadata.package,
    author=metadata.authors[0],
    author_email = metadata.emails[0],
    maintainer=metadata.authors[0],
    maintainer_email=metadata.emails[0],
    url=metadata.url,
    version=metadata.version,
    description=metadata.description,
    long_description=read('README.md'),
    keywords = metadata.keywords,
    # Find a list of classifiers here:
    # <http://pypi.python.org/pypi?%3Aaction=list_classifiers>
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Software Distribution',
    ],
    packages=find_packages(exclude=(TESTS_DIRECTORY)),
    license='LICENSE.txt',
    install_requires=[
        'hexdump == 2.0',
        'hurry.filesize == 0.9',
        'yapsy == 1.10.323',
        'pyxdg == 0.25',
        'sphinxcontrib-napoleon == 0.2.7'
    ],
    tests_require=[
        'pytest==2.5.2',
        'mock==1.0.1',
        'flake8==2.1.0',
    ],
    entry_points={
        'console_scripts': [
            'rawdisk = rawdisk.main:main',
        ]        
    }
)

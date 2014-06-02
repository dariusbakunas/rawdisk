# -*- coding: utf-8 -*-
import os
import sys
import imp
import subprocess
from setuptools import setup, find_packages

## Python 2.6 subprocess.check_output compatibility. Thanks Greg Hewgill!
if 'check_output' not in dir(subprocess):
    def check_output(cmd_args, *args, **kwargs):
        proc = subprocess.Popen(
            cmd_args, *args,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
        out, err = proc.communicate()
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(args)
        return out
    subprocess.check_output = check_output

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

# Helper functions
def git_ls_files(*cmd_args):
    """Run ``git ls-files`` in the top-level project directory. Arguments go
    directly to execution call.

    Returns:
        set of file names
    """
    cmd = ['git', 'ls-files']
    cmd.extend(cmd_args)
    return set(subprocess.check_output(cmd).splitlines())

def get_git_project_files():
    """Retrieve a list of all non-ignored files, including untracked files,
    excluding deleted files.

    Returns:
        sorted list of git project files
    """
    cached_and_untracked_files = git_ls_files(
        '--cached',  # All files cached in the index
        '--others',  # Untracked files
        # Exclude untracked files that would be excluded by .gitignore, etc.
        '--exclude-standard')
    uncommitted_deleted_files = git_ls_files('--deleted')

    # Since sorting of files in a set is arbitrary, return a sorted list to
    # provide a well-defined order to tools like flake8, etc.
    return sorted(cached_and_untracked_files - uncommitted_deleted_files)

def is_git_project():
    return os.path.isdir('.git')

def get_project_files():
    """Retrieve a list of project files, ignoring hidden files.

    Returns:
        sorted list of project files
    """
    if is_git_project():
        return get_git_project_files()

    project_files = []
    for top, subdirs, files in os.walk('.'):
        for subdir in subdirs:
            if subdir.startswith('.'):
                subdirs.remove(subdir)

        for f in files:
            if f.startswith('.'):
                continue
            project_files.append(os.path.join(top, f))

    return project_files

def read(filename):
    """Return the contents of a file.

    :param filename: file path
    :type filename: :class:`str`
    :return: the file's content
    :rtype: :class:`str`
    """
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()

setup_dict = dict(
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

def main():
    setup(**setup_dict)

if __name__ == '__main__':
    main()

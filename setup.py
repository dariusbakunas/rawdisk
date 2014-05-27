import os
from setuptools import setup, find_packages

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
    name='rawdisk',
    author='D. Bakunas',
    version='0.2dev',
    description='Experimental python code to learn different disk formats',
    packages=find_packages(),
    package_data = {'rawdisk.plugins.filesystems' : ['*.yapsy-plugin']},
    license='LICENSE.txt',
    long_description=read('README.md'),
    install_requires=[
        'hexdump >= 2.0',
        'hurry.filesize >= 0.9',
        'yapsy >= 1.10.323',
        'pyxdg >= 0.25'
    ],
    entry_points={
        'console_scripts': [
            'rawdisk = rawdisk.main:main',
        ]        
    }
)

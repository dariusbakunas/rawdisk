from setuptools import setup, find_packages

setup(
    name='rawdisk',
    author='D. Bakunas',
    version='0.1dev',
    description='Experimental python code to learn different disk formats',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    install_requires=[
        'hexdump >= 2.0',
        'hurry.filesize >= 0.9'
    ],
    entry_points={
        'console_scripts': [
            'rawdisk = rawdisk.main:main',
        ]        
    }
)

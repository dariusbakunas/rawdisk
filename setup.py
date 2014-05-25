from setuptools import setup, find_packages

setup(
    name='rawdisk',
    author='D. Bakunas',
    version='0.2dev',
    description='Experimental python code to learn different disk formats',
    packages=find_packages(),
    package_data = {'rawdisk.plugins.filesystems' : ['*.yapsy-plugin']},
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    install_requires=[
        'hexdump >= 2.0',
        'hurry.filesize >= 0.9',
        'yapsy >= 1.10.323'
    ],
    entry_points={
        'console_scripts': [
            'rawdisk = rawdisk.main:main',
        ]        
    }
)

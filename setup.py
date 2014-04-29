from distutils.core import setup

setup(
    name='rawdisk',
    author='D. Bakunas'
    version='0.1dev',
    description='Experimental python code to learn different disk formats',
    packages=['rawdisk',],
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    install_requires=[
        "hexdump >= 2.0",
    ]
)

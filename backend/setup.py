from setuptools import setup

setup(
    name='gaspi',
    version='0.1-snapshot',
    packages=['classes'],
    url='',
    license='beer',
    author='faebser',
    author_email='fabian.frei@esf-frei.ch',
    description='gaspi.ch',
    install_requires=['pystache', 'logging', 'markdown2', 'scss', 'Pillow']
)

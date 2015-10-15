from distutils.core import setup
from setuptools import find_packages

dependencies = [
    'argparse==1.2.1',
    'funcsigs==0.4',
    'mock==1.3.0',
    'pbr==1.8.1',
    'requests==2.8.1',
    'six==1.10.0',
    'wsgiref==0.1.2',
]

setup(
    name='python-timesync',
    version='0.0.1',
    install_requires=dependencies,
    author=u'OSU Open Source Lab',
    author_email='support@osuosl.org',
    packages=find_packages(),
    url='https://github.com/osuosl/python-timesync',
    license='Apache Version 2.0',
    zip_safe=False,
    description="python module for TimeSync API",
    long_description=open('README.md').read()
)

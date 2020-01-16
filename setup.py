try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

dependencies = [
    'argparse==1.2.1',
    'funcsigs==0.4',
    'pbr==1.8.1',
    'requests==2.20.0',
    'six==1.10.0',
    'bcrypt==3.1.7',
]

setup(
    name='pymesync',
    version='0.2.0',
    install_requires=dependencies,
    author='OSU Open Source Lab',
    author_email='support@osuosl.org',
    packages=['pymesync'],
    url='https://github.com/osuosl/pymesync',
    license='Apache Version 2.0',
    description="pymesync - python module for the OSUOSL TimeSync API",
    long_description=("pymesync - Python module for interacting with the "
                      "OSUOSL TimeSync API")
)

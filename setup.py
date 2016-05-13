from distutils.core import setup

dependencies = [
    'argparse==1.2.1',
    'funcsigs==0.4',
    'mock==1.3.0',
    'pbr==1.8.1',
    'requests==2.8.1',
    'six==1.10.0',
    'wsgiref==0.1.2',
    'bcrypt==2.0.0',
]

setup(
    name='pymesync',
    version='0.1.4',
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

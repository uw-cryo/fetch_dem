#!/usr/bin/env python

from distutils.core import setup

setup(name='fetch_dem',
      version='0.1',
      description='Utility to request, download, and process a user-specified region of the global DEMs available via OpenTopography API.',
      author='Shashank Bhushan, David Shean, Scott Henderson',
      author_email='sbaglapl@uw.edu',
      license='MIT',
      long_description=open('README.md').read(),
      url='https://github.com/uw-cryo/fetch_dem.git',
      packages=['fetch_dem'],
      install_requires=['requests']
      )
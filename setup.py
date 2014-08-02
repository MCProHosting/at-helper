import os
import sys

from setuptools import setup, find_packages
from distutils.sysconfig import get_python_lib

setup(
    name='at-helper',
    version='0.0.0',
    url='https://github.com/MCProHosting/at-helper',
    author='Connor Peet',
    author_email='connor@connorpeet.com',
    description=('Open source implementation of the ATLauncher server compilation process.'),
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires = ['requests', 'lxml'],
    classifiers=[]
)
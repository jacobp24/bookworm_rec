"""
Code to Find Packages for Bookworm Recommendations
"""
from setuptools import setup, find_packages

setup(
    name='your_package_name',
    version='1.0',
    packages=find_packages(include=['bookworm', 'bookworm.*']),
    # You can also use 'exclude' to exclude certain directories
    # packages=find_packages(exclude=['data_raw']),
    # Other setup configurations...
)

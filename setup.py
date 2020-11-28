# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in speedex/__init__.py
from speedex import __version__ as version

setup(
	name='speedex',
	version=version,
	description='Custom app for speedex',
	author='bizmap',
	author_email='pathakujjwal93@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

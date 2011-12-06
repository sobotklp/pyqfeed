#!/usr/bin/env python
import os, sys, re, pkg_resources
from distutils.core import setup

# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
try:
    import setuptools
except ImportError:
    pass

kwargs = {}

major, minor = sys.version_info[:2]
if major >= 3:
    import setuptools  # setuptools is required for use_2to3
    kwargs["use_2to3"] = True

# patch distutils if it can't cope with the "classifiers" or "download_url"
# keywords (prior to python 2.3.0).
from distutils.dist import DistributionMetadata
if not hasattr(DistributionMetadata, 'classifiers'):
	DistributionMetadata.classifiers = None
if not hasattr(DistributionMetadata, 'download_url'):
	DistributionMetadata.download_url = None

project_name = 'pyqfeed'
from pyqfeed import version

if __name__ == "__main__":
		setup(
			name = project_name,
			version = version,
			description = 'Python interface to IQFeed financial data',
			author = 'Lewis Sobotkiewicz',
			author_email = 'lewis.sobot@gmail.com',
			platforms=['POSIX', 'Windows'],
			test_suite = 'nose.collector',
			tests_require=['nose>=1.1.2'],
			packages=setuptools.find_packages(),
			package_dir = {'pyqfeed' : 'pyqfeed' },
			**kwargs
		)


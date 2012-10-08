#!/usr/bin/env python
from setuptools import setup

from pyqfeed import __version__

if __name__ == "__main__":
		setup(
			name = 'pyqfeed',
			version = __version__,
			description = 'Python interface to IQFeed financial data',
			author = 'Lewis Sobotkiewicz',
			author_email = 'lewis.sobot@gmail.com',
			platforms=['POSIX', 'Windows'],
			test_suite = 'tests',
			packages=['pyqfeed'],
			use_2to3 = True,
			classifiers = [
				'Intended Audience :: Developers',
				'Operating System :: OS Independent',
				'Programming Language :: Python',
				'License :: OSI Approved :: MIT License',
				'Programming Language :: Python :: 2.5',
				'Programming Language :: Python :: 2.6',
				'Programming Language :: Python :: 2.7',
				'Programming Language :: Python :: 3.2',
				'Programming Language :: Python :: 3.3',
				'Programming Language :: Python :: Implementation :: PyPy',
				'Topic :: Software Development :: Libraries',
				'Topic :: Software Development :: Libraries :: Python Modules',
			],
		)


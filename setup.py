from distutils.core import setup

# patch distutils if it can't cope with the "classifiers" or "download_url"
# keywords (prior to python 2.3.0).
from distutils.dist import DistributionMetadata
if not hasattr(DistributionMetadata, 'classifiers'):
	DistributionMetadata.classifiers = None
if not hasattr(DistributionMetadata, 'download_url'):
	DistributionMetadata.download_url = None

setup(
	name = 'pyqfeed',
	version = '0.1',
	description = 'PyQFeed',
	author = 'Lewis Sobotkiewicz',
	author_email = 'lewis.sobot@gmail.com',
	platforms=['POSIX', 'Windows'],
	packages=['pyqfeed'],
	package_dir = {'pyqfeed' : 'pyqfeed' },
)


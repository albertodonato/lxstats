#
# This file is part of ProcSys.
#
# ProcSys is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# ProcSys is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ProcSys.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

from procsys import __version__, __doc__ as description


config = {
    'name': 'procsys',
    'version': __version__,
    'license': 'GPLv3+',
    'description': description,
    'long_description': open('README.rst').read(),
    'author': 'Alberto Donato',
    'author_email': 'alberto.donato@gmail.com',
    'maintainer': 'Alberto Donato',
    'maintainer_email': 'alberto.donato@gmail.com',
    'url': 'https://bitbucket.org/ack/procsys',
    'download_url': 'https://bitbucket.org/ack/procsys/downloads',
    'packages': find_packages(),
    'include_package_data': True,
    "entry_points": {
        "console_scripts": ["procs = procsys.scripts.procs:script"]},
    'test_suite': 'procsys',
    'install_requires': ['toolrack = 1.0.1', 'prettytable'],
    'keywords': 'linux proc sys performance monitoring system admin',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Operating System :: POSIX :: Linux'
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Benchmark',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities']}

setup(**config)

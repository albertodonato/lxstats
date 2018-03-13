from pathlib import Path
from setuptools import (
    find_packages,
    setup,
)

from lxstats import (
    __doc__ as description,
    __version__,
)


config = {
    'name': 'lxstats',
    'version': __version__,
    'license': 'LGPLv3+',
    'description': description,
    'long_description': Path('README.rst').read_text(),
    'author': 'Alberto Donato',
    'author_email': 'alberto.donato@gmail.com',
    'maintainer': 'Alberto Donato',
    'maintainer_email': 'alberto.donato@gmail.com',
    'url': 'https://github.com/albertodonato/lxstats',
    'packages': find_packages(),
    'include_package_data': True,
    "entry_points": {
        "console_scripts": ["procs = lxstats.scripts.procs:script"]},
    'test_suite': 'lxstats',
    'install_requires': ['prettytable', 'toolrack >= 2.0.1'],
    'keywords': 'linux proc sys performance monitoring system admin',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        ('License :: OSI Approved :: '
         'GNU Lesser General Public License v3 or later (LGPLv3+)'),
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Benchmark',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities']}

setup(**config)

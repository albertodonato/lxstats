from pathlib import Path

from setuptools import (
    find_packages,
    setup,
)

tests_require = ['pytest', 'pytest-mock']

config = {
    'name': 'lxstats',
    'version': '0.3.0',
    'license': 'LGPLv3+',
    'description': (
        'Library to interact with files under /proc and /sys on Linux'),
    'long_description': Path('README.rst').read_text(),
    'packages': find_packages(include=['lxstats', 'lxstats.*']),
    'include_package_data': True,
    "entry_points": {
        "console_scripts": ["procs = lxstats.scripts.procs:script"]
    },
    'test_suite': 'lxstats',
    'install_requires': ['prettytable', 'toolrack >= 2.0.1'],
    'keywords': 'linux proc sys performance monitoring system admin',
    'extras_require': {
        'testing': tests_require
    },
    'classifiers': [
        'Development Status :: 4 - Beta', 'Environment :: Console',
        'Intended Audience :: System Administrators',
        (
            'License :: OSI Approved :: '
            'GNU Lesser General Public License v3 or later (LGPLv3+)'),
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Benchmark', 'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Systems Administration', 'Topic :: Utilities'
    ]
}

setup(**config)

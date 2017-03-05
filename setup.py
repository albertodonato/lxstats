from setuptools import setup, find_packages

from lxstats import __version__, __doc__ as description


config = {
    'name': 'lxstats',
    'version': __version__,
    'license': 'GPLv3+',
    'description': description,
    'long_description': open('README.rst').read(),
    'author': 'Alberto Donato',
    'author_email': 'alberto.donato@gmail.com',
    'maintainer': 'Alberto Donato',
    'maintainer_email': 'alberto.donato@gmail.com',
    'url': 'https://bitbucket.org/ack/lxstats',
    'download_url': 'https://bitbucket.org/ack/lxstats/downloads',
    'packages': find_packages(),
    'include_package_data': True,
    "entry_points": {
        "console_scripts": ["procs = lxstats.scripts.procs:script"]},
    'test_suite': 'lxstats',
    'install_requires': ['prettytable', 'toolrack >= 1.0.1'],
    'keywords': 'linux proc sys performance monitoring system admin',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Operating System :: POSIX :: Linux'
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Benchmark',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities']}

setup(**config)

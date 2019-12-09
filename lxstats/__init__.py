"""Library to interact with files under /proc and /sys on Linux."""

from distutils.version import LooseVersion

import pkg_resources

__all__ = ["__version__"]

__version__ = LooseVersion(pkg_resources.require("lxstats")[0].version)

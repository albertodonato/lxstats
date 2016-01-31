#
# This file is part of LxStats.
#
# LxStats is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# LxStats is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# LxStats.  If not, see <http://www.gnu.org/licenses/>.

'''Read and write files under /proc and /sys Linux filesystems.

This module and its submoduels contain specialized classes to read, parse and
write content to different types of files under /proc and /sys Linux
filesystems.

Submodules are structured as follows:

 - :mod:`lxstats.files.text`: base classes for reading and writing text files.

 - :mod:`lxstats.files.types`: classes for reading and writing different types
   of files, mostly used in the /sys filesystem

'''

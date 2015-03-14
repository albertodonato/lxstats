#
# This file is part of ProcSys.

# ProcSys is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# ProcSys is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ProcSys.  If not, see <http://www.gnu.org/licenses/>.

'''Classes mapping file and directories.'''


import os


class File(object):
    '''Wrapper to reaad/write a file.'''

    def __init__(self, path):
        self.path = path

    def read(self):
        '''Return file content.'''
        with open(self.path) as fh:
            return fh.read()

    def write(self, content):
        '''Write content to file.'''
        with open(self.path, 'w') as fh:
            fh.write(content)


class Directory(object):
    '''Exposes a collection of Files with a dict-like interface.'''

    # Subclasses should define this as dict mapping file names to File type
    files = {}

    def __init__(self, path):
        self.path = path

    def list(self):
        '''Return a list of names in the directory.'''
        return sorted(
            name for name in self.files if os.path.exists(self._path(name)))

    def __getitem__(self, name):
        '''Return the File instance for a name.'''
        path = self._path(name)
        if not os.path.exists(path):
            raise KeyError(name)
        return self.files[name](path)

    def _path(self, name):
        return os.path.join(self.path, name)

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

'''Classes mapping file and directories.'''


import os


class Entity:
    '''Base class for File and Directory.'''

    def __init__(self, path):
        self.path = path

    def exists(self):
        '''Whether the path exists.'''
        return os.path.exists(self.path)

    def readable(self):
        '''Whether the path is readable.'''
        return os.access(self.path, os.R_OK)

    def writable(self):
        '''Whether the path is writable.'''
        return os.access(self.path, os.W_OK)


class File(Entity):
    '''Wrapper to reaad/write a file.'''

    def read(self):
        '''Return file content.'''
        with open(self.path) as fh:
            return fh.read()

    def write(self, content):
        '''Write content to file.'''
        with open(self.path, 'w') as fh:
            fh.write(content)


class Directory(Entity):
    '''Exposes a collection of Files with a dict-like interface.'''

    # Subclasses should define this as dict mapping file names to File type
    files = {}

    def list(self):
        '''Return a list of names in the directory.'''
        return sorted(
            name for name in self.files if os.path.exists(self._path(name)))

    def listdir(self):
        '''Return all existing names in the Directory.'''
        return os.listdir(self.path)

    def __getitem__(self, name):
        '''Return the File instance for a name.'''
        path = self._path(name)
        item = self.files[name](path)
        if not item.exists():
            raise KeyError(name)
        return item

    def _path(self, name):
        return os.path.join(self.path, name)

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

'''Base unittest classes.'''

import os
from tempfile import mktemp

from fixtures import TestWithFixtures, TempDir

from procsys.process.process import Process


class TestCase(TestWithFixtures):
    '''Base class for tests.'''

    def setUp(self):
        super(TestCase, self).setUp()
        # A base temporary directory
        self.tempdir = self.useFixture(TempDir()).path

    def mktemp(self, suffix='', prefix='procsys-test'):
        '''Wrap tempfile.mktemp.'''
        return mktemp(suffix=suffix, prefix=prefix, dir=self.tempdir)

    def mkdir(self):
        '''Create a temporary directory and return the path.'''
        fixture = self.useFixture(TempDir(rootdir=self.tempdir))
        return fixture.path

    def mkfile(self, path=None, content='', mode=None):
        '''Create a temporary file and return its path.'''
        if path is None:
            path = self.mktemp()

        # Create missing path elements as needed
        dirname = os.path.dirname(path)
        if dirname and not os.path.isdir(dirname):
            os.makedirs(dirname)

        with open(path, 'w') as fh:
            fh.write(content)

        if mode is not None:
            os.chmod(path, mode)
        return path

    def readfile(self, path):
        '''Return the content of the specified file.'''
        with open(path) as fh:
            return fh.read()


class ProcessTestMixin(object):
    '''Mixin class with utilities for testing Process classes.'''

    def make_proc_file(self, pid, name, content='', mode=None):
        '''Create a proc file for the process with the specified content.'''
        path = os.path.join(self.tempdir, str(pid), name)
        self.mkfile(path=path, content=content, mode=mode)

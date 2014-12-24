'''Base unittest classes.'''

import os
from tempfile import mktemp

from fixtures import TestWithFixtures, TempDir


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
        with open(path, 'w') as fh:
            fh.write(content)

        if mode is not None:
            os.chmod(path, mode)
        return path

    def readfile(self, path):
        '''Return the content of the specified file.'''
        with open(path) as fh:
            return fh.read()

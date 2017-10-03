"""Base unittest classes."""

import os

from toolrack.testing import TestCase as ToolRackTestCase
from toolrack.testing.fixtures import TempDirFixture


class TestCase(ToolRackTestCase):
    """Base class for tests."""

    def setUp(self):
        super().setUp()
        # A base temporary directory
        self.tempdir = self.useFixture(TempDirFixture())

    def make_process_file(self, pid, name, content='', mode=None):
        """Create a /proc file for the process with the specified content."""
        path = os.path.join(str(pid), name)
        return self.tempdir.mkfile(path=path, content=content, mode=mode)

    def make_process_dir(self, pid, name):
        """Create a subdirectory under a process /proc directory."""
        path = os.path.join(str(pid), name)
        return self.tempdir.mkdir(path=path)

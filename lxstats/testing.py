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

'''Base unittest classes.'''

import os

from toolrack.testing import TestCase as ToolRackTestCase
from toolrack.testing.fixtures import TempDirFixture


class TestCase(ToolRackTestCase):
    '''Base class for tests.'''

    def setUp(self):
        super().setUp()
        # A base temporary directory
        self.tempdir = self.useFixture(TempDirFixture())

    def make_process_file(self, pid, name, content='', mode=None):
        '''Create a /proc file for the process with the specified content.'''
        path = os.path.join(str(pid), name)
        return self.tempdir.mkfile(path=path, content=content, mode=mode)

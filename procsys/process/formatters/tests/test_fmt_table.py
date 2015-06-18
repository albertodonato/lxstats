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

from io import StringIO

from procsys.testing import TestCase

from procsys.process.formatters import TableFormatter
from procsys.process.collection import Collector, Collection


class TableFormatterTests(TestCase):

    def setUp(self):
        super().setUp()
        self.stream = StringIO()
        collector = Collector(proc=self.tempdir.path, pids=(10, 20))
        self.collection = Collection(collector=collector)
        self.make_process_file(10, 'cmdline', content='/bin/foo')
        self.make_process_file(20, 'cmdline', content='/bin/bar')

    def test_format(self):
        '''TableFormatter outputs a table with processes data.'''
        formatter = TableFormatter(self.stream, ['pid', 'cmd'])
        formatter.format(self.collection)
        self.assertEqual(
            self.stream.getvalue(),
            ' pid  cmd      \n'
            ' 10   /bin/foo \n'
            ' 20   /bin/bar \n')

    def test_format_border(self):
        '''TableFormatter can add borders to the table.'''
        formatter = TableFormatter(
            self.stream, ['pid', 'cmd'], borders=True)
        formatter.format(self.collection)
        self.assertEqual(
            self.stream.getvalue(),
            '+-----+----------+\n'
            '| pid | cmd      |\n'
            '+-----+----------+\n'
            '| 10  | /bin/foo |\n'
            '| 20  | /bin/bar |\n'
            '+-----+----------+\n')

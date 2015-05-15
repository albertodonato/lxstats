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

from io import StringIO

from procsys.testing import TestCase

from procsys.process.formatters import CSVFormatter
from procsys.process.collection import Collector, Collection


class CSVFormatterTests(TestCase):

    def setUp(self):
        super().setUp()
        self.stream = StringIO()
        collector = Collector(proc=self.tempdir, pids=(10, 20))
        self.collection = Collection(collector=collector)
        self.make_process_file(10, 'cmdline', content='/bin/foo')
        self.make_process_file(20, 'cmdline', content='/bin/bar')

    def test_format(self):
        '''CSVFormatter outputs CSV file with processes data.'''
        formatter = CSVFormatter(self.stream, ['pid', 'cmd'])
        formatter.format(self.collection)
        self.assertEqual(
            self.stream.getvalue(),
            'pid,cmd\r\n'
            '10,/bin/foo\r\n'
            '20,/bin/bar\r\n')

    def test_format_tabs(self):
        '''CSVFormatter can use tabs as field separators.'''
        formatter = CSVFormatter(self.stream, ['pid', 'cmd'], tabs=True)
        formatter.format(self.collection)
        self.assertEqual(
            self.stream.getvalue(),
            'pid\tcmd\r\n'
            '10\t/bin/foo\r\n'
            '20\t/bin/bar\r\n')

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

from procsys.testing import TestCase

from procsys.process.process import Process
from procsys.process.filter import CommandLineFilter


class CommandLineFilterTests(TestCase):

    def setUp(self):
        super().setUp()
        self.pid = 10
        self.process = Process(
            self.pid, proc_dir='{}/{}'.format(self.tempdir, self.pid))

    def test_filter_matching_process(self):
        '''CommandLineFilter matches a process.'''
        proc_filter = CommandLineFilter('foo')
        self.make_process_file(
            self.pid, 'cmdline', content='/bin/foo\x00bar\x00')
        self.process.collect_stats()
        self.assertTrue(proc_filter(self.process))

    def test_filter_non_matching_process(self):
        '''CommandLineFilter doesn't match a process.'''
        proc_filter = CommandLineFilter('foo')
        self.make_process_file(
            self.pid, 'cmdline', content='/bin/bar\x00foo\x00')
        self.process.collect_stats()
        self.assertFalse(proc_filter(self.process))

    def test_include_args(self):
        '''Arguments are included in match if include_args is True.'''
        proc_filter = CommandLineFilter('foo', include_args=True)
        self.make_process_file(
            self.pid, 'cmdline', content='/bin/bar\x00foo\x00')
        self.process.collect_stats()
        self.assertTrue(proc_filter(self.process))

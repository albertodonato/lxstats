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

from procsys.testing import TestCase, ProcessTestMixin
from procsys.process.process import Process


class ProcessTests(TestCase, ProcessTestMixin):

    def setUp(self):
        super(ProcessTests, self).setUp()
        self.pid = 10
        self.process = Process(
            self.pid, '{}/{}'.format(self.tempdir, self.pid))

    def test_collect_stats(self):
        '''Stats are collected from proc when collect_stats is called.'''
        self.assertEqual([], self.process.available_stats())
        self.make_proc_file(self.pid, 'cmdline', content='cmd')
        self.process.collect_stats()
        self.assertEqual(self.process.available_stats(), ['cmdline'])

    def test_collect_stats_no_proc_dir(self):
        '''If the process dir is not found, stats are left empty.'''
        self.process.collect_stats()
        self.assertEqual(self.process.available_stats(), [])
        self.assertEqual(self.process.stats(), {})

    def test_collect_stats_prefix(self):
        '''The file prefix is used if it reports multiple stats.'''
        self.make_proc_file(self.pid, 'statm', content='1 2 3 4 5 6 7')
        self.process.collect_stats()
        self.assertEqual(
            self.process.stats(),
            {'statm.size': 1, 'statm.resident': 2, 'statm.share': 3,
             'statm.text': 4, 'statm.lib': 5, 'statm.data': 6, 'statm.dt': 7})

    def test_collect_stats_unreadable_file(self):
        '''Unreadable files are skipped when reading stats.'''
        self.make_proc_file(self.pid, 'cmdline', content='cmd', mode=0o200)
        self.process.collect_stats()
        self.assertEqual(self.process.available_stats(), [])

    def test_cmd_from_cmdline(self):
        '''Process.cmd parses the content of /proc/cmdline if not empty.'''
        self.make_proc_file(self.pid, 'cmdline', content='cmd\0with\0args')
        self.process.collect_stats()
        self.assertNotIn('comm', self.process.available_stats())
        self.assertEqual(self.process['cmdline'], 'cmd with args')
        self.assertEqual(self.process.cmd, 'cmd with args')

    def test_cmd_from_comm(self):
        '''If /proc/cmdline is empty, /proc/cmd is read.'''
        self.make_proc_file(self.pid, 'comm', content='cmd')
        self.process.collect_stats()
        self.assertNotIn('cmdline', self.process.available_stats())
        self.assertEqual(self.process.cmd, '[cmd]')

    def test_cmd_empty(self):
        '''If cmdline and cmd are not found, an empty string is returned.'''
        self.process.collect_stats()
        self.assertEqual(self.process.cmd, '')

    def test_getattr_access_stats(self):
        '''Process stats values can be accessed via __getattr__.'''
        self.make_proc_file(self.pid, 'comm', content='cmd')
        self.process.collect_stats()
        self.assertEqual(self.process['comm'], 'cmd')

    def test_getattr_unknown(self):
        '''Accessing an unknown attribute raises an error.'''
        self.assertRaises(KeyError, self.process.__getitem__, 'unknown')

    def test_available_stats(self):
        '''Available Process stats can be listed.'''
        self.make_proc_file(self.pid, 'comm', content='cmd')
        self.make_proc_file(self.pid, 'wchan', content='0')
        self.process.collect_stats()
        self.assertEqual(self.process.available_stats(), ['comm', 'wchan'])

    def test_stats(self):
        '''Available Process  stats can be returned as a dict .'''
        self.make_proc_file(self.pid, 'comm', content='cmd')
        self.make_proc_file(self.pid, 'wchan', content='0')
        self.process.collect_stats()
        self.assertEqual(self.process.stats(), {'comm': 'cmd', 'wchan': '0'})

    def test_get(self):
        '''Value for a stat can be returned.'''
        self.make_proc_file(self.pid, 'wchan', content='poll_schedule_timeout')
        self.process.collect_stats()
        self.assertEqual(self.process.get('wchan'), 'poll_schedule_timeout')

    def test_get_not_found(self):
        '''If the requested stat is not found, None is returned.'''
        self.process.collect_stats()
        self.assertIsNone(self.process.get('wchan'))

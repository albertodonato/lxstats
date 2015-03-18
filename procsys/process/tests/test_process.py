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

from procsys.testing import TestCase

from procsys.process.process import Process


class ProcessTests(TestCase):

    def setUp(self):
        super(ProcessTests, self).setUp()
        self.pid = 10
        self.process = Process(
            self.pid, '{}/{}'.format(self.tempdir, self.pid))

    def test_exists(self):
        '''It's possible to check whether a process exists.'''
        self.assertFalse(self.process.exists())
        self.make_process_file(self.pid, 'cmdline', content='cmd')
        self.assertTrue(self.process.exists())

    def test_collect_stats(self):
        '''Stats are collected from proc when collect_stats is called.'''
        self.assertEqual([], self.process.available_stats())
        self.make_process_file(self.pid, 'cmdline', content='cmd')
        self.process.collect_stats()
        self.assertEqual(self.process.available_stats(), ['cmdline'])

    def test_collect_stats_no_proc_dir(self):
        '''If the process dir is not found, stats are left empty.'''
        self.process.collect_stats()
        self.assertEqual(self.process.available_stats(), [])
        self.assertEqual(self.process.stats(), {})

    def test_collect_stats_prefix(self):
        '''The file prefix is used if it reports multiple stats.'''
        self.make_process_file(self.pid, 'statm', content='1 2 3 4 5 6 7')
        self.process.collect_stats()
        self.assertEqual(
            self.process.stats(),
            {'statm.size': 1, 'statm.resident': 2, 'statm.share': 3,
             'statm.text': 4, 'statm.lib': 5, 'statm.data': 6, 'statm.dt': 7})

    def test_collect_stats_unreadable_file(self):
        '''Unreadable files are skipped when reading stats.'''
        self.make_process_file(self.pid, 'cmdline', content='cmd', mode=0o200)
        self.process.collect_stats()
        self.assertEqual(self.process.available_stats(), [])

    def test_cmd_from_cmdline(self):
        '''Process.cmd parses the content of /proc/cmdline if not empty.'''
        self.make_process_file(self.pid, 'cmdline', content='cmd\0with\0args')
        self.process.collect_stats()
        self.assertNotIn('comm', self.process.available_stats())
        self.assertEqual(self.process.get('cmdline'), 'cmd with args')
        self.assertEqual(self.process.cmd, 'cmd with args')

    def test_cmd_from_comm(self):
        '''If /proc/cmdline is empty, /proc/cmd is read.'''
        self.make_process_file(self.pid, 'comm', content='cmd')
        self.process.collect_stats()
        self.assertNotIn('cmdline', self.process.available_stats())
        self.assertEqual(self.process.cmd, '[cmd]')

    def test_cmd_empty(self):
        '''If cmdline and cmd are not found, an empty string is returned.'''
        self.process.collect_stats()
        self.assertEqual(self.process.cmd, '')

    def test_available_stats(self):
        '''Available Process stats can be listed.'''
        self.make_process_file(self.pid, 'comm', content='cmd')
        self.make_process_file(self.pid, 'wchan', content='0')
        self.process.collect_stats()
        self.assertEqual(self.process.available_stats(), ['comm', 'wchan'])

    def test_stats(self):
        '''Available Process  stats can be returned as a dict .'''
        self.make_process_file(self.pid, 'comm', content='cmd')
        self.make_process_file(self.pid, 'wchan', content='0')
        self.process.collect_stats()
        self.assertEqual(self.process.stats(), {'comm': 'cmd', 'wchan': '0'})

    def test_get(self):
        '''Value for a stat can be returned.'''
        self.make_process_file(
            self.pid, 'wchan', content='poll_schedule_timeout')
        self.process.collect_stats()
        self.assertEqual(self.process.get('wchan'), 'poll_schedule_timeout')

    def test_get_not_found(self):
        '''If the requested stat is not found, None is returned.'''
        self.process.collect_stats()
        self.assertIsNone(self.process.get('wchan'))

    def test_get_pid(self):
        '''The get() method can return the PID.'''
        self.process.collect_stats()
        self.assertEqual(self.process.get('pid'), self.process.pid)

    def test_get_cmd(self):
        '''The get() method can return the cmd.'''
        self.make_process_file(self.pid, 'cmdline', content='cmd')
        self.process.collect_stats()
        self.assertEqual(self.process.get('cmd'), 'cmd')

    def test_equal(self):
        '''Two Processes are equal if they have the same pid.'''
        other = Process(
            self.pid, '{}/{}'.format(self.tempdir, self.pid))
        different = Process(
            self.pid + 1, '{}/{}'.format(self.tempdir, self.pid))
        self.assertEqual(self.process, other)
        self.assertNotEqual(self.process, different)

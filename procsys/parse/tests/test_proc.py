#
# This file is part of Procsys.

# Procsys is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Procsys is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Procsys.  If not, see <http://www.gnu.org/licenses/>.

from procsys.testing import TestCase

from procsys.parse.proc import (
    ProcStat, ProcUptime, ProcLoadavg, ProcVmstat, ProcDiskstats,
    ProcPIDStat, ProcPIDStatm)


class ProcStatTests(TestCase):

    def test_cpu_fields(self):
        '''Time counters are reported as percentage per-CPU.'''
        path = self.mkfile(
            content=(
                'cpu0 2.0 0.0 3.0 5.0 7.0 3.0 10.0 20.0 30.0 20.0\n'
                'cpu1 10.0 7.0 5.0 3.0 0.0 3.0 2.0 30.0 20.0 20.0\n'))
        parser = ProcStat(path)
        self.assertEqual(
            parser.parse(),
            {'cpu0': {
                'user': 0.02, 'nice': 0.0, 'system': 0.03, 'idle': 0.05,
                'iowait': 0.07, 'irq': 0.03, 'softirq': 0.1, 'steal': 0.2,
                'guest': 0.3, 'guest-nice': 0.2},
             'cpu1': {
                'user': 0.1, 'nice': 0.07, 'system': 0.05, 'idle': 0.03,
                'iowait': 0.00, 'irq': 0.03, 'softirq': 0.02, 'steal': 0.3,
                'guest': 0.2, 'guest-nice': 0.2}})

    def test_not_all_cpu_fields(self):
        '''Some CPU fields may be missing.'''
        path = self.mkfile(
            content='cpu0 20.0 10.0 30.0 20.0 7.0 3.0 10.0\n')
        parser = ProcStat(path)
        self.assertEqual(
            parser.parse(),
            {'cpu0': {
                'user': 0.2, 'nice': 0.1, 'system': 0.3, 'idle': 0.2,
                'iowait': 0.07, 'irq': 0.03, 'softirq': 0.1}})

    def test_ignore_non_cpu_fields(self):
        '''Extra fields after CPU ones are ignored.'''
        path = self.mkfile(
            content=(
                'cpu0 20.0 10.0 30.0 20.0 7.0 3.0 10.0\nanother row\n'))
        parser = ProcStat(path)
        self.assertEqual(
            parser.parse(),
            {'cpu0': {
                'user': 0.2, 'nice': 0.1, 'system': 0.3, 'idle': 0.2,
                'iowait': 0.07, 'irq': 0.03, 'softirq': 0.1}})


class ProcUptimeTests(TestCase):

    def test_fields(self):
        '''Uptime and idle times are reported.'''
        path = self.mkfile(content='67569.47 106913.77')
        parser = ProcUptime(path)
        self.assertEqual(
            parser.parse(), {'uptime': 67569.47, 'idle': 106913.77})


class ProcLoadavgTests(TestCase):

    def test_fields(self):
        '''Load average over 1, 5, and 15 minutes is reported.'''
        path = self.mkfile(content='0.40 0.30 0.20')
        parser = ProcLoadavg(path)
        self.assertEqual(
            parser.parse(),
            {'load1': 0.40, 'load5': 0.30, 'load15': 0.20})


class ProcVmstatTests(TestCase):

    def test_fields(self):
        '''Fields and values from the /proc/vmstat file are reported.'''
        path = self.mkfile(content='foo 123\nbar 456')
        parser = ProcVmstat(path)
        self.assertEqual(parser.parse(), {'foo': 123, 'bar': 456})


class ProcDiskstatsTest(TestCase):

    def test_fields(self):
        '''Fields for each device/partition are reported.'''
        path = self.mkfile(
            content=(
                '8 0 sda 10 20 30 40 50 60 70 80 90 100 110\n'
                '8 1 sda1 1 2 3 4 5 6 7 8 9 10 11\n'))
        parser = ProcDiskstats(path)
        self.assertEqual(
            parser.parse(),
            {'sda': {
                'read': 10, 'read-merged': 20, 'read-sect': 30, 'read-ms': 40,
                'write': 50, 'write-merged': 60, 'write-sect': 70,
                'write-ms': 80, 'io-curr': 90, 'io-ms': 100,
                'io-ms-weighted': 110},
             'sda1': {
                'read': 1, 'read-merged': 2, 'read-sect': 3, 'read-ms': 4,
                'write': 5, 'write-merged': 6, 'write-sect': 7, 'write-ms': 8,
                'io-curr': 9, 'io-ms': 10, 'io-ms-weighted': 11}})


class ProcPIDStatTests(TestCase):

    def test_fields(self):
        '''Fields and values from /proc/[pid]/stat files are reported.'''
        content = ' '.join(str(i) for i in range(45))
        path = self.mkfile(content=content)
        parser = ProcPIDStat(path)
        self.assertEqual(
            parser.parse(),
            {'state': '2',
             'ppid': 3,
             'pgrp': 4,
             'session': 5,
             'tty_nr': 6,
             'tpgid': 7,
             'flags': 8,
             'minflt': 9,
             'cminflt': 10,
             'majflt': 11,
             'cmajflt': 12,
             'utime': 13,
             'stime': 14,
             'cutime': 15,
             'cstime': 16,
             'priority': 17,
             'nice': 18,
             'num_threads': 19,
             'itrealvalue': 20,
             'starttime': 21,
             'vsize': 22,
             'rss': 23,
             'rsslim': 24,
             'startcode': 25,
             'endcode': 26,
             'startstack': 27,
             'kstkesp': 28,
             'kstkeip': 29,
             'exit_signal': 37,
             'processor': 38,
             'rt_priority': 39,
             'policy': 40,
             'delayacct_blkio_ticks': 41,
             'guest_time': 42,
             'cguest_time': 43})


class ProcPIDStatmTests(TestCase):

    def test_fields(self):
        '''Fields and values from /proc/[pid]/statm files are reported.'''
        path = self.mkfile(content='1 2 3 4 5 6 7')
        parser = ProcPIDStatm(path)
        self.assertEqual(
            parser.parse(),
            {'size': 1, 'resident': 2, 'share': 3, 'text': 4, 'lib': 5,
             'data': 6, 'dt': 7})

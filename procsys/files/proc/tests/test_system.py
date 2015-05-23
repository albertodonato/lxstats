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

from procsys.files.proc.system import (
    ProcStat, ProcUptime, ProcLoadavg, ProcVmstat, ProcDiskstats, ProcMeminfo)


class ProcStatTests(TestCase):

    def test_cpu_fields(self):
        '''Time counters are reported as percentage per-CPU.'''
        path = self.mkfile(
            content=(
                'cpu0 2.0 0.0 3.0 5.0 7.0 3.0 10.0 20.0 30.0 20.0\n'
                'cpu1 10.0 7.0 5.0 3.0 0.0 3.0 2.0 30.0 20.0 20.0\n'))
        stat_file = ProcStat(path)
        self.assertEqual(
            stat_file.read(),
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
        stat_file = ProcStat(path)
        self.assertEqual(
            stat_file.read(),
            {'cpu0': {
                'user': 0.2, 'nice': 0.1, 'system': 0.3, 'idle': 0.2,
                'iowait': 0.07, 'irq': 0.03, 'softirq': 0.1}})

    def test_ignore_non_cpu_fields(self):
        '''Extra fields after CPU ones are ignored.'''
        path = self.mkfile(
            content=(
                'cpu0 20.0 10.0 30.0 20.0 7.0 3.0 10.0\nanother row\n'))
        stat_file = ProcStat(path)
        self.assertEqual(
            stat_file.read(),
            {'cpu0': {
                'user': 0.2, 'nice': 0.1, 'system': 0.3, 'idle': 0.2,
                'iowait': 0.07, 'irq': 0.03, 'softirq': 0.1}})


class ProcUptimeTests(TestCase):

    def test_fields(self):
        '''Uptime and idle times are reported.'''
        path = self.mkfile(content='67569.47 106913.77')
        uptime_file = ProcUptime(path)
        self.assertEqual(
            uptime_file.read(), {'uptime': 67569.47, 'idle': 106913.77})


class ProcLoadavgTests(TestCase):

    def test_fields(self):
        '''Load average over 1, 5, and 15 minutes is reported.'''
        path = self.mkfile(content='0.40 0.30 0.20')
        loadavg_file = ProcLoadavg(path)
        self.assertEqual(
            loadavg_file.read(),
            {'load1': 0.40, 'load5': 0.30, 'load15': 0.20})


class ProcVmstatTests(TestCase):

    def test_fields(self):
        '''Fields and values from the /proc/vmstat file are reported.'''
        path = self.mkfile(content='foo 123\nbar 456')
        vmstat_file = ProcVmstat(path)
        self.assertEqual(vmstat_file.read(), {'foo': 123, 'bar': 456})


class ProcDiskstatsTests(TestCase):

    def test_fields(self):
        '''Fields for each device/partition are reported.'''
        path = self.mkfile(
            content=(
                '8 0 sda 10 20 30 40 50 60 70 80 90 100 110\n'
                '8 1 sda1 1 2 3 4 5 6 7 8 9 10 11\n'))
        diskstats_file = ProcDiskstats(path)
        self.assertEqual(
            diskstats_file.read(),
            {'sda': {
                'read': 10, 'read-merged': 20, 'read-sect': 30, 'read-ms': 40,
                'write': 50, 'write-merged': 60, 'write-sect': 70,
                'write-ms': 80, 'io-curr': 90, 'io-ms': 100,
                'io-ms-weighted': 110},
             'sda1': {
                'read': 1, 'read-merged': 2, 'read-sect': 3, 'read-ms': 4,
                'write': 5, 'write-merged': 6, 'write-sect': 7, 'write-ms': 8,
                'io-curr': 9, 'io-ms': 10, 'io-ms-weighted': 11}})


class ProcMeminfoTests(TestCase):

    def test_fields(self):
        '''Each line in the file /proc/meminfo file is reported.'''
        path = self.mkfile(
            content=(
                'MemTotal:       1000 kB\n'
                'MemFree:         200 kB\n'
                'HugePages_Total:   0\n'))
        meminfo_file = ProcMeminfo(path)
        self.assertEqual(
            meminfo_file.read(),
            {'MemTotal': 1000, 'MemFree': 200, 'HugePages_Total': 0})

from textwrap import dedent

from ....testing import TestCase
from ..system import (
    ProcStat, ProcUptime, ProcLoadavg, ProcVmstat, ProcDiskstats, ProcMeminfo,
    ProcCgroups)


class ProcStatTests(TestCase):

    def test_cpu_fields(self):
        """Time counters are reported as percentage per-CPU."""
        path = self.tempdir.mkfile(
            content=(
                'cpu0 2.0 0.0 3.0 5.0 7.0 3.0 10.0 20.0 30.0 20.0\n'
                'cpu1 10.0 7.0 5.0 3.0 0.0 3.0 2.0 30.0 20.0 20.0\n'))
        stat_file = ProcStat(path)
        self.assertEqual(
            stat_file.parse(),
            {'cpu0': {
                'user': 0.02, 'nice': 0.0, 'system': 0.03, 'idle': 0.05,
                'iowait': 0.07, 'irq': 0.03, 'softirq': 0.1, 'steal': 0.2,
                'guest': 0.3, 'guest-nice': 0.2},
             'cpu1': {
                'user': 0.1, 'nice': 0.07, 'system': 0.05, 'idle': 0.03,
                'iowait': 0.00, 'irq': 0.03, 'softirq': 0.02, 'steal': 0.3,
                'guest': 0.2, 'guest-nice': 0.2}})

    def test_not_all_cpu_fields(self):
        """Some CPU fields may be missing."""
        path = self.tempdir.mkfile(
            content='cpu0 20.0 10.0 30.0 20.0 7.0 3.0 10.0\n')
        stat_file = ProcStat(path)
        self.assertEqual(
            stat_file.parse(),
            {'cpu0': {
                'user': 0.2, 'nice': 0.1, 'system': 0.3, 'idle': 0.2,
                'iowait': 0.07, 'irq': 0.03, 'softirq': 0.1}})

    def test_ignore_non_cpu_fields(self):
        """Extra fields after CPU ones are ignored."""
        path = self.tempdir.mkfile(
            content=(
                'cpu0 20.0 10.0 30.0 20.0 7.0 3.0 10.0\nanother row\n'))
        stat_file = ProcStat(path)
        self.assertEqual(
            stat_file.parse(),
            {'cpu0': {
                'user': 0.2, 'nice': 0.1, 'system': 0.3, 'idle': 0.2,
                'iowait': 0.07, 'irq': 0.03, 'softirq': 0.1}})


class ProcUptimeTests(TestCase):

    def test_fields(self):
        """Uptime and idle times are reported."""
        path = self.tempdir.mkfile(content='67569.47 106913.77')
        uptime_file = ProcUptime(path)
        self.assertEqual(
            uptime_file.parse(), {'uptime': 67569.47, 'idle': 106913.77})


class ProcLoadavgTests(TestCase):

    def test_fields(self):
        """Load average over 1, 5, and 15 minutes is reported."""
        path = self.tempdir.mkfile(content='0.40 0.30 0.20')
        loadavg_file = ProcLoadavg(path)
        self.assertEqual(
            loadavg_file.parse(),
            {'load1': 0.40, 'load5': 0.30, 'load15': 0.20})


class ProcVmstatTests(TestCase):

    def test_fields(self):
        """Fields and values from the /proc/vmstat file are reported."""
        path = self.tempdir.mkfile(content='foo 123\nbar 456')
        vmstat_file = ProcVmstat(path)
        self.assertEqual(vmstat_file.parse(), {'foo': 123, 'bar': 456})


class ProcDiskstatsTests(TestCase):

    def test_fields(self):
        """Fields for each device/partition are reported."""
        path = self.tempdir.mkfile(
            content=dedent(
                '''\
                8 0 sda 10 20 30 40 50 60 70 80 90 100 110
                8 1 sda1 1 2 3 4 5 6 7 8 9 10 11
                '''))
        diskstats_file = ProcDiskstats(path)
        self.assertEqual(
            diskstats_file.parse(),
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
        """Each line in the file /proc/meminfo file is reported."""
        path = self.tempdir.mkfile(
            content=dedent(
                '''\
                MemTotal:       1000 kB
                MemFree:         200 kB
                HugePages_Total:   0
                '''))
        meminfo_file = ProcMeminfo(path)
        self.assertEqual(
            meminfo_file.parse(),
            {'MemTotal': 1000, 'MemFree': 200, 'HugePages_Total': 0})


class ProcCgroupsTests(TestCase):

    def test_fields(self):
        """Each line in the file /proc/cgroups file is reported."""
        path = self.tempdir.mkfile(
            content=dedent(
                '''\
                #subsys_name    hierarchy       num_cgroups     enabled
                cpuset  10      200     1
                cpu     3       100     0
                cpuacct 3       300     1
                '''))
        cgroups_file = ProcCgroups(path)
        self.assertEqual(
            cgroups_file.parse(),
            {'cpuset': {
                'hierarchy-id': 10, 'num-cgroups': 200, 'enabled': True},
             'cpu': {
                 'hierarchy-id': 3, 'num-cgroups': 100, 'enabled': False},
             'cpuacct': {
                'hierarchy-id': 3, 'num-cgroups': 300,  'enabled': True}})

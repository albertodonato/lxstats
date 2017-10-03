from textwrap import dedent

from ....testing import TestCase
from ..process import (
    ProcPIDCmdline, ProcPIDStat, ProcPIDStatm, ProcPIDIo, ProcPIDSched,
    ProcPIDEnviron, ProcPIDCgroup)


class ProcPIDCmdlineTests(TestCase):

    def test_parse(self):
        """Command line tokens are parsed and split into a list."""
        path = self.tempdir.mkfile(content='/bin/foo\x00bar\x00baz\x00')
        cmdline_file = ProcPIDCmdline(path)
        self.assertEqual(cmdline_file.parse(), ['/bin/foo', 'bar', 'baz'])

    def test_parse_with_spaces(self):
        """Command or arguments can contain spaces."""
        path = self.tempdir.mkfile(content='/bin/foo bar\x00baz bza\x00')
        cmdline_file = ProcPIDCmdline(path)
        self.assertEqual(cmdline_file.parse(), ['/bin/foo bar', 'baz bza'])


class ProcPIDStatTests(TestCase):

    def test_fields(self):
        """Fields and values from /proc/[pid]/stat files are reported."""
        content = ' '.join(str(i) for i in range(45))
        path = self.tempdir.mkfile(content=content)
        stat_file = ProcPIDStat(path)
        self.assertEqual(
            stat_file.parse(),
            {'pid': 0,
             'comm': '1',
             'state': '2',
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

    def test_comm_with_spaces(self):
        """The comm field can contain spaces.."""
        fields = [str(i) for i in range(45)]
        # Set a comm field with spaces
        fields[1] = '(cmd with spaces)'
        content = ' '.join(fields)
        path = self.tempdir.mkfile(content=content)
        stat_file = ProcPIDStat(path)
        stats = stat_file.parse()
        self.assertEqual(stats['comm'], 'cmd with spaces')


class ProcPIDStatmTests(TestCase):

    def test_fields(self):
        """Fields and values from /proc/[pid]/statm files are reported."""
        path = self.tempdir.mkfile(content='1 2 3 4 5 6 7')
        statm_file = ProcPIDStatm(path)
        self.assertEqual(
            statm_file.parse(),
            {'size': 1, 'resident': 2, 'share': 3, 'text': 4, 'lib': 5,
             'data': 6, 'dt': 7})


class ProcPIDIOTests(TestCase):

    def test_fields(self):
        """Fields and values from /proc/[pid]/io files are reported."""
        content = dedent(
            '''\
            rchar: 100
            wchar: 200
            syscr: 300
            syscw: 400
            read_bytes: 500
            write_bytes: 600
            cancelled_write_bytes: 700
            ''')
        path = self.tempdir.mkfile(content=content)
        io_file = ProcPIDIo(path)
        self.assertEqual(
            io_file.parse(),
            {'rchar': 100,
             'wchar': 200,
             'syscr': 300,
             'syscw': 400,
             'read_bytes': 500,
             'write_bytes': 600,
             'cancelled_write_bytes': 700})


class ProcPIDSchedTests(TestCase):

    def test_fields(self):
        """Fields and values from /proc/[pid]/sched files are parsed."""
        content = dedent(
            '''\
            process (1234, #threads: 1)
            -------------------------------------------------------------------
            se.exec_start                                :     123456789.123456
            se.vruntime                                  :       1234567.123456
            se.sum_exec_runtime                          :             0.123456
            se.statistics.sum_sleep_runtime              :             1.234567
            current_node=0, numa_group_id=0
            numa_faults node=0 task_private=0 task_shared=0 group_private=0
            ''')
        path = self.tempdir.mkfile(content=content)
        io_file = ProcPIDSched(path)
        self.assertEqual(
            io_file.parse(),
            {'se.exec_start': 123456789.123456,
             'se.vruntime': 1234567.123456,
             'se.sum_exec_runtime': 0.123456,
             'se.statistics.sum_sleep_runtime': 1.234567})


class ProcPIDEnvironTests(TestCase):

    def test_parse(self):
        """Environment variables are returned as a dict."""
        path = self.tempdir.mkfile(content='FOO=foo\x00BAR=bar\x00')
        environ_file = ProcPIDEnviron(path)
        self.assertEqual(environ_file.parse(), {'FOO': 'foo', 'BAR': 'bar'})

    def test_parse_single_value(self):
        """If the = sign is not present, the line is used as key."""
        path = self.tempdir.mkfile(content='someline\x00BAR=bar\x00')
        environ_file = ProcPIDEnviron(path)
        self.assertEqual(
            environ_file.parse(), {'someline': None, 'BAR': 'bar'})


class ProcPIDCgroupTests(TestCase):

    def test_parse(self):
        """A dict is returned with hierarchy id as key."""
        content = dedent(
            '''\
            6:hugetlb:/group2
            5:net_cls,net_prio:/group1
            4:blkio:/group2
            3:cpu,cpuacct:/group1
            2:devices:/group1
            ''')
        path = self.tempdir.mkfile(content=content)
        cgroup_file = ProcPIDCgroup(path)
        self.assertEqual(
            cgroup_file.parse(),
            {6: (['hugetlb'], '/group2'),
             5: (['net_cls', 'net_prio'], '/group1'),
             4: (['blkio'], '/group2'),
             3: (['cpu', 'cpuacct'], '/group1'),
             2: (['devices'], '/group1')})

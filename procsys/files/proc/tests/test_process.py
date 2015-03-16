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

from textwrap import dedent

from procsys.testing import TestCase

from procsys.files.proc.process import ProcPIDStat, ProcPIDStatm, ProcPIDIo


class ProcPIDStatTests(TestCase):

    def test_fields(self):
        '''Fields and values from /proc/[pid]/stat files are reported.'''
        content = ' '.join(str(i) for i in range(45))
        path = self.mkfile(content=content)
        parser = ProcPIDStat(path)
        self.assertEqual(
            parser.parse(),
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


class ProcPIDStatmTests(TestCase):

    def test_fields(self):
        '''Fields and values from /proc/[pid]/statm files are reported.'''
        path = self.mkfile(content='1 2 3 4 5 6 7')
        parser = ProcPIDStatm(path)
        self.assertEqual(
            parser.parse(),
            {'size': 1, 'resident': 2, 'share': 3, 'text': 4, 'lib': 5,
             'data': 6, 'dt': 7})


class ProcPIDIOTests(TestCase):

    def test_fields(self):
        '''Fields and values from /proc/[pid]/io files are reported.'''
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
        path = self.mkfile(content=content)
        parser = ProcPIDIo(path)
        self.assertEqual(
            parser.parse(),
            {'rchar': 100,
             'wchar': 200,
             'syscr': 300,
             'syscw': 400,
             'read_bytes': 500,
             'write_bytes': 600,
             'cancelled_write_bytes': 700})

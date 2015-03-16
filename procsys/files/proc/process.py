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

'''Parsers for per-process files under /proc/[pid]/.'''

from procsys.files.text import ParsedFile, SingleLineFile


class ProcPIDCmdline(ParsedFile):
    '''Parse /proc/[pid]/cmdline.'''

    def parser(self, content):
        return content.replace('\x00', ' ').strip()


class ProcPIDStat(SingleLineFile):
    '''Parse /proc/[pid]/stat and /proc/[pid]/tasks/[tid]/stat.'''

    fields = (
        ('pid', int),
        ('comm', str),
        ('state', str),
        ('ppid', int),
        ('pgrp', int),
        ('session', int),
        ('tty_nr', int),
        ('tpgid', int),
        ('flags', int),
        ('minflt', int),
        ('cminflt', int),
        ('majflt', int),
        ('cmajflt', int),
        ('utime', int),
        ('stime', int),
        ('cutime', int),
        ('cstime', int),
        ('priority', int),
        ('nice', int),
        ('num_threads', int),
        ('itrealvalue', int),
        ('starttime', int),
        ('vsize', int),
        ('rss', int),
        ('rsslim', int),
        ('startcode', int),
        ('endcode', int),
        ('startstack', int),
        ('kstkesp', int),
        ('kstkeip', int),
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ('exit_signal', int),
        ('processor', int),
        ('rt_priority', int),
        ('policy', int),
        ('delayacct_blkio_ticks', int),
        ('guest_time', int),
        ('cguest_time', int))


class ProcPIDStatm(SingleLineFile):
    '''Parse /proc/[pid]/statm.'''

    fields = (
        ('size', int),
        ('resident', int),
        ('share', int),
        ('text', int),
        ('lib', int),
        ('data', int),
        ('dt', int))


class ProcPIDIo(ParsedFile):
    '''Parse /proc/[pid]/io.'''

    def parser(self, content):
        # Each line is in the form "name: count".
        result = {}
        for line in content.splitlines():
            key, value = line.split(': ', 1)
            result[key] = int(value)
        return result

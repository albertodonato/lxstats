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

'''Parsers for Linux /proc files.'''

from procsys.parse.text import FileParser, SingleLineFileParser


class ProcStat(FileParser):
    '''Parse /proc/stat'''

    stat_fields = [
        'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq', 'steal',
        'guest', 'guest-nice']

    def parser(self, lines):
        result = {}

        for line in lines:
            if not line.startswith('cpu'):
                # Only CPU stats are reported for now.
                break

            values = line.split()
            label = values.pop(0)
            values = [float(value) for value in values]
            total = sum(values)
            values = [(value / total) for value in values]
            # If there are less fields than the declared ones, they are ignored
            # by zip().
            result[label] = dict(zip(self.stat_fields, values))
        return result


class ProcUptime(SingleLineFileParser):
    '''Parser for /proc/uptime'''

    fields = (('uptime', float), ('idle', float))


class ProcLoadavg(SingleLineFileParser):
    '''Parser for /proc/loadavg'''

    fields = (('load1', float), ('load5', float), ('load15', float))


class ProcVmstat(FileParser):
    '''Parser for /proc/vmstat'''

    def parser(self, lines):
        items = (line.split() for line in lines)
        return dict((key, int(value)) for key, value in items)


class ProcDiskstats(FileParser):
    '''Parser for /proc/diskstats'''

    diskstat_fields = [
        'read', 'read-merged', 'read-sect', 'read-ms', 'write', 'write-merged',
        'write-sect', 'write-ms', 'io-curr', 'io-ms', 'io-ms-weighted']

    def parser(self, lines):
        result = {}
        for line in lines:
            split = line.split()[2:]  # Ignore major/minor fields
            dev_name, values = split[0], split[1:]
            values = [int(value) for value in values]
            result[dev_name] = dict(zip(self.diskstat_fields, values))
        return result


class ProcPIDStat(SingleLineFileParser):
    '''Parser for /proc/[pid]/stat and /proc/[pid]/tasks/[tid]/stat.'''

    fields = (
        None,
        None,
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


class ProcPIDStatm(SingleLineFileParser):
    '''Parser for /proc/[pid]/statm.'''

    fields = (
        ('size', int),
        ('resident', int),
        ('share', int),
        ('text', int),
        ('lib', int),
        ('data', int),
        ('dt', int))


class ProcPIDIo(FileParser):
    '''Parser for /proc/[pid]/io.'''

    def parser(self, lines):
        # Each line eis in the form "name: count".
        result = {}
        for line in lines:
            key, value = line.split(': ', 1)
            result[key] = int(value)
        return result

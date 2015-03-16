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

'''Parsers for /proc files containing system information.'''

from procsys.files.text import ParsedFile, SingleLineFile


class ProcStat(ParsedFile):
    '''Parse /proc/stat'''

    stat_fields = [
        'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq', 'steal',
        'guest', 'guest-nice']

    def parser(self, content):
        result = {}

        for line in content.splitlines():
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


class ProcUptime(SingleLineFile):
    '''Parser for /proc/uptime'''

    fields = (('uptime', float), ('idle', float))


class ProcLoadavg(SingleLineFile):
    '''Parser for /proc/loadavg'''

    fields = (('load1', float), ('load5', float), ('load15', float))


class ProcVmstat(ParsedFile):
    '''Parser for /proc/vmstat'''

    def parser(self, content):
        items = (line.split() for line in content.splitlines())
        return dict((key, int(value)) for key, value in items)


class ProcDiskstats(ParsedFile):
    '''Parser for /proc/diskstats'''

    diskstat_fields = [
        'read', 'read-merged', 'read-sect', 'read-ms', 'write', 'write-merged',
        'write-sect', 'write-ms', 'io-curr', 'io-ms', 'io-ms-weighted']

    def parser(self, content):
        result = {}
        for line in content.splitlines():
            split = line.split()[2:]  # Ignore major/minor fields
            dev_name, values = split[0], split[1:]
            values = [int(value) for value in values]
            result[dev_name] = dict(zip(self.diskstat_fields, values))
        return result

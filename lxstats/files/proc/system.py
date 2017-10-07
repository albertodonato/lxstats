"""Parsers for :file:`/proc` files containing system information."""

import re

from ..text import (
    ParsedFile,
    SingleLineFile)


class ProcStat(ParsedFile):
    """Parse :file:`/proc/stat`."""

    stat_fields = [
        'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq', 'steal',
        'guest', 'guest-nice']

    def _parse(self, content):
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
    """Parse :file:`/proc/uptime`."""

    fields = (('uptime', float), ('idle', float))


class ProcLoadavg(SingleLineFile):
    """Parse :file:`/proc/loadavg`."""

    fields = (('load1', float), ('load5', float), ('load15', float))


class ProcVmstat(ParsedFile):
    """Parse :file:`/proc/vmstat`."""

    def _parse(self, content):
        items = (line.split() for line in content.splitlines())
        return dict((key, int(value)) for key, value in items)


class ProcDiskstats(ParsedFile):
    """Parse :file:`/proc/diskstats`."""

    diskstat_fields = [
        'read', 'read-merged', 'read-sect', 'read-ms', 'write', 'write-merged',
        'write-sect', 'write-ms', 'io-curr', 'io-ms', 'io-ms-weighted']

    def _parse(self, content):
        result = {}
        for line in content.splitlines():
            split = line.split()[2:]  # Ignore major/minor fields
            dev_name, values = split[0], split[1:]
            values = [int(value) for value in values]
            result[dev_name] = dict(zip(self.diskstat_fields, values))
        return result


class ProcMeminfo(ParsedFile):
    """Parse :file:`/proc/meminfo`."""

    _parse_re = re.compile(r'(?P<name>.+):\s+(?P<value>[0-9]+)')

    def _parse(self, content):
        return dict(self._parse_line(line) for line in content.splitlines())

    def _parse_line(self, line):
        match = self._parse_re.match(line).groupdict()
        return match['name'], int(match['value'])


class ProcCgroups(ParsedFile):
    """Parse :file:`/proc/cgroups`."""

    def _parse(self, content):
        result = {}
        for line in content.splitlines():
            if line.startswith('#'):
                continue
            subsys, hier_id, num_cgroups, enabled = line.split()
            result[subsys] = {
                'hierarchy-id': int(hier_id),
                'num-cgroups': int(num_cgroups),
                'enabled': enabled == '1'}
        return result

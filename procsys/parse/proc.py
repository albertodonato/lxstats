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

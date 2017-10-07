"""Parsers for per-process files under :file:`/proc/[pid]/`."""

import re

from ..text import (
    ParsedFile,
    SingleLineFile)


class ProcPIDCmdline(SingleLineFile):
    """Parse :file:`/proc/[pid]/cmdline`."""

    separator = '\x00'


class ProcPIDStat(SingleLineFile):
    """Parse :file:`/proc/[pid]/stat`, :file:`/proc/[pid]/tasks/[tid]/stat`."""

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

    _re = re.compile('\((.+)\)')

    def separator(self, content):
        """Custom separator to handle spaces in the process commandline."""

        content = content.strip(' ')
        match = self._re.search(content)
        if match is None:
            return content.split()

        # Replace with a version without spaces so split works
        content = self._re.sub('comm', content)
        split = content.split()
        # Replace the original comm value
        split[1] = match.groups()[0]
        return split


class ProcPIDStatm(SingleLineFile):
    """Parse :file:`/proc/[pid]/statm`."""

    fields = (
        ('size', int),
        ('resident', int),
        ('share', int),
        ('text', int),
        ('lib', int),
        ('data', int),
        ('dt', int))


class ProcPIDIo(ParsedFile):
    """Parse :file:`/proc/[pid]/io`."""

    def _parse(self, content):
        # Each line is in the form 'name: count'.
        result = {}
        for line in content.splitlines():
            key, value = line.split(': ', 1)
            result[key] = int(value)
        return result


class ProcPIDSched(ParsedFile):
    """Parse :file:`/proc/[pid]/sched`."""

    _re = re.compile(r'^(\S+)\s+:\s+(\S+)$')

    def _parse(self, content):
        stats = {}
        for line in content.split('\n'):
            match = self._re.match(line)
            if match:
                key, value = match.groups()
                value = float(value) if '.' in value else int(value)
                stats[key] = value

        return stats


class ProcPIDEnviron(ParsedFile):
    """Parse :file:`/proc/[pid]/environ`."""

    def _parse(self, content):
        # Return a dict with the environment.
        environ = {}
        for line in content.split('\x00'):
            if not line:
                continue

            split = line.split('=', 1)
            environ[split[0]] = None if len(split) == 1 else split[1]

        return environ


class ProcPIDCgroup(ParsedFile):
    """Parse :file:`/proc/[pid]/cgroup`."""

    def _parse(self, content):
        result = {}
        for line in content.splitlines():
            hier_id, subsys, control_group = line.split(':')
            result[int(hier_id)] = (subsys.split(','), control_group)

        return result


class ProcPIDStatus(ParsedFile):
    """Parse :file:`/proc/[pid]/status`."""

    _re = re.compile(':\s+')

    def _parse(self, content):
        tokens = [
            self._re.split(line, maxsplit=1) for line in content.splitlines()]
        return {
            key: int(value[:-3]) * 1024 for key, value in tokens
            if value.endswith(' kB')}

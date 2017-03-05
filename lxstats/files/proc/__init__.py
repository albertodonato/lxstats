'''Access system and process statistics through files under :file:`/proc`.

System statistics, such as load, uptime, memory and disk information can be
read through the :class:`ProcDirectory`. For example::

  >>> ProcDirectory('/proc')['uptime'].parse()
  {'uptime': 695283.06, 'idle': 1376159.44}

Process-specific stats, like used memory, IO, etc. can be accessed through
:class:`ProcProcessDirectory`, such as::

  >>> ProcProcessDirectory('/proc/self')['io'].parse()
  {'rchar': 405786, 'syscr': 415, 'cancelled_write_bytes': 0, 'syscw': 256,
   'write_bytes': 20480, 'read_bytes': 32768, 'wchar': 14790}

'''

from ...fs import Directory
from ..types import ValueFile
from .system import (
    ProcDiskstats,
    ProcLoadavg,
    ProcMeminfo,
    ProcStat,
    ProcVmstat,
    ProcUptime,
    ProcCgroups)
from .process import (
    ProcPIDCmdline,
    ProcPIDIo,
    ProcPIDStat,
    ProcPIDStatm,
    ProcPIDEnviron,
    ProcPIDSched,
    ProcPIDCgroup)


class ProcDirectory(Directory):
    '''The :file:`/proc` directory.'''

    files = {
        'cgroups': ProcCgroups,
        'diskstats': ProcDiskstats,
        'loadavg': ProcLoadavg,
        'meminfo': ProcMeminfo,
        'vmstat': ProcVmstat,
        'stat': ProcStat,
        'uptime': ProcUptime,
        'vmstat': ProcVmstat}


class ProcProcessDirectory(Directory):
    '''A directory for a process under :file:`/proc/[pid]`.'''

    files = {
        'cgroup': ProcPIDCgroup,
        'cmdline': ProcPIDCmdline,
        'comm': ValueFile,
        'environ': ProcPIDEnviron,
        'io': ProcPIDIo,
        'sched': ProcPIDSched,
        'stat': ProcPIDStat,
        'statm': ProcPIDStatm,
        'task': Directory,
        'wchan': ValueFile}


class ProcTaskDirectory(Directory):
    '''A directory for a task under :file:`/proc/[pid]/task/[tid]`.'''

    files = {
        'cgroup': ProcPIDCgroup,
        'cmdline': ProcPIDCmdline,
        'comm': ValueFile,
        'environ': ProcPIDEnviron,
        'io': ProcPIDIo,
        'sched': ProcPIDSched,
        'stat': ProcPIDStat,
        'statm': ProcPIDStatm,
        'wchan': ValueFile}

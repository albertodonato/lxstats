#
# This file is part of LxStats.
#
# LxStats is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# LxStats is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# LxStats.  If not, see <http://www.gnu.org/licenses/>.

'''Access system and process statistics through files under /proc.

System statistics, such as load, uptime, memory and disk information can be
read through the :class:`ProcDirectory`. For example::

  >>> ProcDirectory('/proc')['uptime'].read()
  {'uptime': 695283.06, 'idle': 1376159.44}

Process-specific stats, like used memory, IO, etc. can be accessed through
:class:`ProcPIDDirectory`, such as::

  >>> ProcPIDDirectory('/proc/self')['io'].read()
  {'rchar': 405786, 'syscr': 415, 'cancelled_write_bytes': 0, 'syscw': 256,
   'write_bytes': 20480, 'read_bytes': 32768, 'wchar': 14790}

'''

from ...fs import Directory
from ..types import ValueFile
from .system import (
    ProcDiskstats, ProcLoadavg, ProcMeminfo, ProcStat, ProcVmstat, ProcUptime)
from .process import (
    ProcPIDCmdline, ProcPIDIo, ProcPIDStat, ProcPIDStatm, ProcPIDEnviron,
    ProcPIDSched)


class ProcDirectory(Directory):
    '''The /proc directory.'''

    files = {
        'diskstats': ProcDiskstats,
        'loadavg': ProcLoadavg,
        'meminfo': ProcMeminfo,
        'vmstat': ProcVmstat,
        'stat': ProcStat,
        'uptime': ProcUptime,
        'vmstat': ProcVmstat}


class ProcPIDDirectory(Directory):
    '''A /proc/[pid] directory for a process.'''

    files = {
        'cmdline': ProcPIDCmdline,
        'comm': ValueFile,
        'environ': ProcPIDEnviron,
        'io': ProcPIDIo,
        'sched': ProcPIDSched,
        'stat': ProcPIDStat,
        'statm': ProcPIDStatm,
        'wchan': ValueFile}

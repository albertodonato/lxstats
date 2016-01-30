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

'''Files for parsing Linux /proc files.'''

from ...fs import Directory
from ..types import ValueFile
from .system import (
    ProcDiskstats, ProcLoadavg, ProcMeminfo, ProcStat, ProcVmstat, ProcUptime)
from .process import (
    ProcPIDCmdline, ProcPIDIo, ProcPIDStat, ProcPIDStatm, ProcPIDEnviron)


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
        'stat': ProcPIDStat,
        'statm': ProcPIDStatm,
        'wchan': ValueFile}

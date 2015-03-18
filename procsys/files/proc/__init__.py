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

'''Files for parsing Linux /proc files.'''

from procsys.fs import Directory

from procsys.files.types import ValueFile
from procsys.files.proc.system import (
    ProcDiskstats, ProcLoadavg, ProcStat, ProcVmstat, ProcUptime)
from procsys.files.proc.process import (
    ProcPIDCmdline, ProcPIDIo, ProcPIDStat, ProcPIDStatm)


class ProcDirectory(Directory):
    '''The /proc directory.'''

    files = {
        'diskstats': ProcDiskstats,
        'loadavg': ProcLoadavg,
        'vmstat': ProcVmstat,
        'stat': ProcStat,
        'uptime': ProcUptime,
        'vmstat': ProcVmstat}


class ProcPIDDirectory(Directory):
    '''A /proc/[pid] directory for a process.'''

    files = {
        'cmdline': ProcPIDCmdline,
        'comm': ValueFile,
        'io': ProcPIDIo,
        'stat': ProcPIDStat,
        'statm': ProcPIDStatm,
        'wchan': ValueFile}

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

'''Files for parsing Linux /sys files.'''

from procsys.fs import Directory, File
from procsys.files.types import (
    OptionsFile, ValueFile, ToggleFile, SelectableOptionsFile,
    TogglableOptionsFile)


class TracingDirectory(Directory):
    '''A /sys/kernel/debug/tracing/instance/[tracer] directory.'''

    files = {
        'available_tracers': OptionsFile,
        'current_tracer': ValueFile,
        'trace_clock': SelectableOptionsFile,
        'trace_options': TogglableOptionsFile,
        'trace_marker': File,
        'tracing_on': ToggleFile
    }

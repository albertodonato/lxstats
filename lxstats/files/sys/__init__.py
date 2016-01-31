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

'''Access files under the /sys filesytem.

This module currently allows to access and configure tracing options via
:class:`TracingDirectory`.

'''

from ...fs import Directory, File
from ..types import (
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

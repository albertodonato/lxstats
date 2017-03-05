'''Access files under the :file:`/sys` filesytem.

This module currently allows to access and configure tracing options via
:class:`TracingDirectory`.

'''

from ...fs import Directory, File
from ..types import (
    OptionsFile, ValueFile, ToggleFile, SelectableOptionsFile,
    TogglableOptionsFile)


class TracingDirectory(Directory):
    '''A :file:`/sys/kernel/debug/tracing/instance/[tracer]` directory.'''

    files = {
        'available_tracers': OptionsFile,
        'current_tracer': ValueFile,
        'trace_clock': SelectableOptionsFile,
        'trace_options': TogglableOptionsFile,
        'trace_marker': File,
        'tracing_on': ToggleFile
    }

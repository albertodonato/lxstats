#
# This file is part of ProcSys.
#
# ProcSys is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# ProcSys is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ProcSys.  If not, see <http://www.gnu.org/licenses/>.

'''Interface to kernel tracing.'''

import os

from procsys.files.sys import TracingDirectory
from procsys.tracing.types import TRACER_TYPES


class Tracing:
    '''Interface to kernel tracing.'''

    def __init__(self, path='/sys/kernel/debug/tracing'):
        self.path = path

    @property
    def tracers(self):
        '''List of current tracing instances in alphabetical order.'''
        names = sorted(os.listdir(os.path.join(self.path, 'instances')))
        return [self.get_tracer(name) for name in names]

    def get_tracer(self, name):
        '''Return a Tracer.

        If the name doesn't match an existing tracer, a new one is added.

        '''
        tracer_path = self._tracer_path(name)
        if not os.path.isdir(tracer_path):
            os.mkdir(tracer_path)
        return Tracer(tracer_path)

    def remove_tracer(self, name):
        '''Remove the tracer with the specified name.'''
        os.rmdir(self._tracer_path(name))

    def _tracer_path(self, name):
        return os.path.join(self.path, 'instances', name)


class Tracer:
    '''A kernel tracing instance.'''

    def __init__(self, path):
        self.path = path
        self._dir = TracingDirectory(path)

    @property
    def name(self):
        '''The tracer name.'''
        return os.path.basename(self.path)

    @property
    def type(self):
        ''''Return the current tracer type.'''
        return self._dir['current_tracer'].value

    def set_type(self, tracer_type):
        '''Set the type of the tracer.'''
        self._dir['current_tracer'].set(tracer_type)

    @property
    def enabled(self):
        '''Whether the tracer is enabled.'''
        return self._dir['tracing_on'].enabled

    def toggle(self, status):
        '''Enable or disable the tracer.'''
        self._dir['tracing_on'].toggle(status)

    @property
    def options(self):
        '''Return a dict with tracing options and their status.'''
        return self._dir['trace_options'].options

    def set_option(self, option, value):
        '''Set the value of a strcing option.'''
        self._dir['trace_options'].toggle(option, value)

    @property
    def _tracer(self):
        '''Return a TracerType for the current tracer.'''
        try:
            return TRACER_TYPES.get(self.type)
        except KeyError:
            return None

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

'''Linux kernel tracer types.'''

from toolrack.collect import Collection

from ..files.sys import TracingDirectory


# Available tracer types
TRACER_TYPES = Collection('TracerType', 'name')


class TracerType:
    '''Base class for tracer types.'''

    name = None

    def __init__(self, path):
        self.path = path
        self._dir = TracingDirectory(path)


@TRACER_TYPES.add
class NopTracer(TracerType):
    '''No-op tracer.'''

    name = 'nop'

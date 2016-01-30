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

from unittest import TestCase

from ...files.sys import TracingDirectory
from ...tracing.types import TracerType, TRACER_TYPES, NopTracer


class TracerTypeTests(TestCase):

    def test_path(self):
        '''A TracerType has a path and a TracingDirectory pointing to it.'''
        tracer_type = TracerType('/foo/bar')
        self.assertEqual(tracer_type.path, '/foo/bar')
        self.assertIsInstance(tracer_type._dir, TracingDirectory)
        self.assertEqual(tracer_type._dir.path, '/foo/bar')


class TracerTypesTyests(TestCase):

    def test_tracer_types_registry(self):
        '''TRACER_TYPES is a registry of available TracerTypes.'''
        self.assertIs(TRACER_TYPES.get('nop'), NopTracer)

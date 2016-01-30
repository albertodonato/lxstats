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

from os import path

from ...testing import TestCase
from ...tracing.tracer import UnsupportedTracer, Tracing, Tracer


class TracingTests(TestCase):

    def setUp(self):
        super().setUp()
        self.tracing = Tracing(path=self.tempdir.path)
        self.tempdir.mkdir(path='instances')

    def test_tracers_empty(self):
        '''If no tracer is defined, an empty list is returned.'''
        self.assertEqual(self.tracing.tracers, [])

    def test_tracers_exists(self):
        '''A Tracer object is returned for each tracing directory.'''
        self.tempdir.mkdir(path='instances/tracer-1')
        self.tempdir.mkdir(path='instances/tracer-2')
        for tracer in self.tracing.tracers:
            self.assertIsInstance(tracer, Tracer)
        self.assertEqual(
            [tracer.name for tracer in self.tracing.tracers],
            ['tracer-1', 'tracer-2'])

    def test_get_tracer_existing(self):
        '''A Tracer for a specified tracing instance is returned.'''
        self.tempdir.mkdir(path='instances/tracer')
        tracer = self.tracing.get_tracer('tracer')
        self.assertEqual(tracer.name, 'tracer')

    def test_get_tracer_create(self):
        '''If the requested tracing instance doesn't exist, it's created.'''
        self.tracing.get_tracer('tracer')
        instance_path = path.join(self.tempdir.path, 'instances/tracer')
        self.assertTrue(path.exists(instance_path))

    def test_remove_tracer(self):
        '''A Tracer can be removed.'''
        self.tempdir.mkdir(path='instances/tracer')
        instance_path = path.join(self.tempdir.path, 'instances/tracer')
        self.tracing.remove_tracer('tracer')
        self.assertFalse(path.exists(instance_path))


class TracerTests(TestCase):

    def setUp(self):
        super().setUp()
        self.tracer = Tracer(path=self.tempdir.path)

    def test_name(self):
        '''The Tracer name is the name of the tracer directory.'''
        name = path.basename(self.tempdir.path)
        self.assertEqual(self.tracer.name, name)

    def test_type(self):
        '''The Tracer type can be returned.'''
        self.tempdir.mkfile(path='current_tracer', content='nop')
        self.assertEqual(self.tracer.type, 'nop')

    def test_set_type(self):
        '''The Tracer type can be set.'''
        self.tempdir.mkfile(path='current_tracer', content='func')
        self.tracer.set_type('nop')
        self.assertEqual(self.tracer.type, 'nop')

    def test_set_type_unsupported(self):
        '''If the Tracer type is unsupported, an error is raised.'''
        self.assertRaises(UnsupportedTracer, self.tracer.set_type, 'unknown')

    def test_enabled_true(self):
        '''The Tracer is enabled if the corresponding flag is set.'''
        self.tempdir.mkfile(path='tracing_on', content='1')
        self.assertTrue(self.tracer.enabled)

    def test_enabled_false(self):
        '''The Tracer is enabled if the corresponding flag is not set.'''
        self.tempdir.mkfile(path='tracing_on', content='0')
        self.assertFalse(self.tracer.enabled)

    def test_toggle(self):
        '''The Tracer can be enabled and disabled.'''
        self.tempdir.mkfile(path='tracing_on', content='0')
        self.tracer.toggle(True)
        self.assertTrue(self.tracer.enabled)
        self.tracer.toggle(False)
        self.assertFalse(self.tracer.enabled)

    def test_options(self):
        '''Tracer options are returned, with their status.'''
        self.tempdir.mkfile(path='trace_options', content='noraw\nhex')
        self.assertEqual({'raw': False, 'hex': True}, self.tracer.options)

    def test_set_option(self):
        '''Tracer options can be set.'''
        self.tempdir.mkfile(path='trace_options', content='nohex')
        self.assertEqual({'hex': False}, self.tracer.options)
        self.tracer.set_option('hex', True)
        self.assertEqual({'hex': True}, self.tracer.options)
        self.tracer.set_option('hex', False)
        self.assertEqual({'hex': False}, self.tracer.options)

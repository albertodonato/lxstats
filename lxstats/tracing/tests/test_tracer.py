from os import path

from toolrack.collect import Collection

from ...testing import TestCase
from ...tracing.tracer import (
    UnsupportedTracer,
    Tracing,
    Tracer)
from ...tracing.types import TracerType


class TracingTests(TestCase):

    def setUp(self):
        super().setUp()
        self.tracing = Tracing(path=self.tempdir.path)
        self.tempdir.mkdir(path='instances')

    def test_tracers_empty(self):
        """If no tracer is defined, an empty list is returned."""
        self.assertEqual(self.tracing.tracers, [])

    def test_tracers_exists(self):
        """A Tracer object is returned for each tracing directory."""
        self.tempdir.mkdir(path='instances/tracer-1')
        self.tempdir.mkdir(path='instances/tracer-2')
        for tracer in self.tracing.tracers:
            self.assertIsInstance(tracer, Tracer)
        self.assertEqual(
            [tracer.name for tracer in self.tracing.tracers],
            ['tracer-1', 'tracer-2'])

    def test_get_tracer_existing(self):
        """A Tracer for a specified tracing instance is returned."""
        self.tempdir.mkdir(path='instances/tracer')
        tracer = self.tracing.get_tracer('tracer')
        self.assertEqual(tracer.name, 'tracer')

    def test_get_tracer_create(self):
        """If the requested tracing instance doesn't exist, it's created."""
        self.tracing.get_tracer('tracer')
        instance_path = path.join(self.tempdir.path, 'instances/tracer')
        self.assertTrue(path.exists(instance_path))

    def test_remove_tracer(self):
        """A Tracer can be removed."""
        self.tempdir.mkdir(path='instances/tracer')
        instance_path = path.join(self.tempdir.path, 'instances/tracer')
        self.tracing.remove_tracer('tracer')
        self.assertFalse(path.exists(instance_path))


class TracerTests(TestCase):

    def setUp(self):
        super().setUp()
        self.tracer = Tracer(path=self.tempdir.path)

    def test_name(self):
        """The Tracer name is the name of the tracer directory."""
        name = path.basename(self.tempdir.path)
        self.assertEqual(self.tracer.name, name)

    def test_type(self):
        """The Tracer type can be returned."""
        self.tempdir.mkfile(path='current_tracer', content='nop')
        self.assertEqual(self.tracer.type, 'nop')

    def test_set_type(self):
        """The Tracer type can be set."""
        self.tempdir.mkfile(path='current_tracer', content='func')
        self.tracer.set_type('nop')
        self.assertEqual(self.tracer.type, 'nop')

    def test_set_type_unsupported(self):
        """If the Tracer type is unsupported, an error is raised."""
        self.assertRaises(UnsupportedTracer, self.tracer.set_type, 'unknown')

    def test_enabled_true(self):
        """The Tracer is enabled if the corresponding flag is set."""
        self.tempdir.mkfile(path='tracing_on', content='1')
        self.assertTrue(self.tracer.enabled)

    def test_enabled_false(self):
        """The Tracer is enabled if the corresponding flag is not set."""
        self.tempdir.mkfile(path='tracing_on', content='0')
        self.assertFalse(self.tracer.enabled)

    def test_toggle(self):
        """The Tracer can be enabled and disabled."""
        self.tempdir.mkfile(path='tracing_on', content='0')
        self.tracer.toggle(True)
        self.assertTrue(self.tracer.enabled)
        self.tracer.toggle(False)
        self.assertFalse(self.tracer.enabled)

    def test_options(self):
        """Tracer options are returned, with their status."""
        self.tempdir.mkfile(path='trace_options', content='noraw\nhex')
        self.assertEqual({'raw': False, 'hex': True}, self.tracer.options)

    def test_set_option(self):
        """Tracer options can be set."""
        self.tempdir.mkfile(path='trace_options', content='nohex')
        self.assertEqual({'hex': False}, self.tracer.options)
        self.tracer.set_option('hex', True)
        self.assertEqual({'hex': True}, self.tracer.options)
        self.tracer.set_option('hex', False)
        self.assertEqual({'hex': False}, self.tracer.options)

    def test_trace_content(self):
        """The trace file content can be returned."""
        self.tempdir.mkfile(path='trace', content='some trace content')
        self.assertEqual('some trace content', self.tracer.trace())

    def test_trace_pipe(self):
        """The trace_pipe file cam be returned and read."""
        self.tempdir.mkfile(path='trace_pipe', content='some trace content')
        with self.tracer.trace_pipe() as pipe:
            self.assertEqual('some trace content', pipe.read())

    def test_attribute_access(self):
        """Attribute specific to the tracer type can be accessed."""

        class SampleTracer(TracerType):

            name = 'sample'

            foo = 'a sample attribute'

        self.tracer._tracer_types = Collection('TracerType', 'name')
        self.tracer._tracer_types.add(SampleTracer)

        self.tempdir.mkfile(path='current_tracer')
        self.tracer.set_type('sample')
        self.assertEqual(self.tracer.foo, 'a sample attribute')

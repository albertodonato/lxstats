from unittest import TestCase

from ...files.sys import TracingDirectory
from ...tracing.types import (
    TracerType,
    TRACER_TYPES,
    NopTracer)


class TracerTypeTests(TestCase):

    def test_path(self):
        """A TracerType has a path and a TracingDirectory pointing to it."""
        tracer_type = TracerType('/foo/bar')
        self.assertEqual(tracer_type.path, '/foo/bar')
        self.assertIsInstance(tracer_type._dir, TracingDirectory)
        self.assertEqual(tracer_type._dir.path, '/foo/bar')


class TracerTypesTyests(TestCase):

    def test_tracer_types_registry(self):
        """TRACER_TYPES is a registry of available TracerTypes."""
        self.assertIs(TRACER_TYPES.get('nop'), NopTracer)

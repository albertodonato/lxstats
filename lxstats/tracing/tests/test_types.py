from pathlib import Path

from ...files.sys import TracingDirectory
from ...tracing.types import (
    NopTracer,
    TRACER_TYPES,
    TracerType,
)


class TestTracerType:

    def test_path(self):
        """A TracerType has a path and a TracingDirectory pointing to it."""
        tracer_type = TracerType('/foo/bar')
        assert tracer_type.path == Path('/foo/bar')
        assert isinstance(tracer_type._dir, TracingDirectory)
        assert tracer_type._dir._path == Path('/foo/bar')


class TestTracerTypes:

    def test_tracer_types_registry(self):
        """TRACER_TYPES is a registry of available TracerTypes."""
        assert TRACER_TYPES.get('nop') is NopTracer

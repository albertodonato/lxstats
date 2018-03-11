"""Interface to kernel tracing."""

from pathlib import Path

from ..files.sys import TracingDirectory
from .types import TRACER_TYPES


class UnsupportedTracer(Exception):
    """Unsupported tracer type specified."""

    def __init__(self, tracer_type):
        self.type = tracer_type
        super().__init__('Unsupported tracer type: {}'.format(tracer_type))


class Tracing:
    """Interface to kernel tracing."""

    def __init__(self, path=Path('/sys/kernel/debug/tracing')):
        self.path = Path(path)

    @property
    def tracers(self):
        """List of current tracing instances in alphabetical order."""
        names = sorted((self.path / 'instances').iterdir())
        return [self.get_tracer(name) for name in names]

    def get_tracer(self, name):
        """Return a Tracer.

        If the name doesn't match an existing tracer, a new one is added.

        """
        tracer_path = self._tracer_path(name)
        if not tracer_path.is_dir():
            tracer_path.mkdir()
        return Tracer(path=tracer_path)

    def remove_tracer(self, name):
        """Remove the tracer with the specified name."""
        self._tracer_path(name).rmdir()

    def _tracer_path(self, name):
        return self.path / 'instances' / name


class Tracer:
    """A kernel tracing instance."""

    _tracer_types = TRACER_TYPES

    def __init__(self, path):
        self.path = Path(path)
        self._dir = TracingDirectory(path)

    def __getattr__(self, attr):
        """Proxy TracerType-specific attributes."""
        return getattr(self._tracer, attr)

    @property
    def name(self):
        """The tracer name."""
        return self.path.name

    @property
    def type(self):
        """'Return the current tracer type."""
        return self._dir['current_tracer'].value

    def set_type(self, tracer_type):
        """Set the type of the tracer."""
        if tracer_type not in self._tracer_types:
            raise UnsupportedTracer(tracer_type)
        self._dir['current_tracer'].set(tracer_type)

    def trace(self):
        """Return content from tracer."""
        return (self.path / 'trace').read_text()

    def trace_pipe(self):
        """Return an open file descript for the tracing output pipe."""
        return (self.path / 'trace_pipe').open()

    @property
    def enabled(self):
        """Whether the tracer is enabled."""
        return self._dir['tracing_on'].enabled

    def toggle(self, status):
        """Enable or disable the tracer."""
        self._dir['tracing_on'].toggle(status)

    @property
    def options(self):
        """Return a dict with tracing options and their status."""
        return self._dir['trace_options'].options

    def set_option(self, option, value):
        """Set the value of a strcing option."""
        self._dir['trace_options'].toggle(option, value)

    @property
    def _tracer(self):
        """TracerType for the current tracer."""
        return self._tracer_types.get(self.type)

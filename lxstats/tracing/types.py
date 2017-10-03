"""Linux kernel tracer types."""

from toolrack.collect import Collection

from ..files.sys import TracingDirectory


# Available tracer types
TRACER_TYPES = Collection('TracerType', 'name')


class TracerType:
    """Base class for tracer types."""

    name = None

    def __init__(self, path):
        self.path = path
        self._dir = TracingDirectory(path)


@TRACER_TYPES.add
class NopTracer(TracerType):
    """No-op tracer."""

    name = 'nop'

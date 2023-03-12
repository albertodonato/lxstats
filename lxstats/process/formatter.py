"""Write field values for a collection of processes in a specific format."""

from collections.abc import Sequence
from typing import (
    Any,
    ClassVar,
    IO,
)

from .collection import Collection
from .process import Process


class Formatter:
    """Format a :class:`Process` :class:`Collection`.

    :param stream: A file-like stream to write the formatted output to.
    :param list fields: Process attributes to print.
    :param dict kwargs: Filter configuration parameters.

    """

    # Name of the format produced by the formatter.
    fmt = ""

    # Configuration parameters with defaults.
    config: ClassVar[dict[str, Any]] = {}

    def __init__(self, stream: IO, fields: Sequence[str], **kwargs):
        self._stream = stream
        self.fields = fields

        unknown_keys = set(kwargs).difference(self.config)
        if unknown_keys:
            keys_list = ", ".join(sorted(unknown_keys))
            raise TypeError(f"Unknown config parameters: {keys_list}")
        self._config = self.config.copy()
        self._config.update(kwargs)

    def _fields_values(self, process: Process) -> list:
        """Return a list of fields values for a :class:`Process`."""
        return [process.get(field) for field in self.fields]

    def format(self, collection: Collection):
        """Write the formatted output of the :class:`Collection`."""
        self._format_header()
        for process in collection:
            self._format_process(process)
        self._format_footer()
        self._dump()

    def _format_header(self):
        """Format the header.

        Subclasses can implement this.

        """
        pass

    def _format_process(self, process: Process):
        """Format data for a :class:`Process`.

        Subclasses can implement this.

        """
        pass

    def _format_footer(self):
        """Format footer.

        Subclasses can implement this.

        """
        pass

    def _dump(self):
        """Dump processed data to the stream.

        Subclasses can implement this.

        """
        pass

    def _write(self, data: str | None):
        if data is not None:
            self._stream.write(data)

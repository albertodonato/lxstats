"""Write field values for a collection of processes in a specific format."""


class Formatter:
    """Format a :class:`Process` :class:`Collection`.

    :param stream: A file-like stream to write the formatted output to.
    :param list fields: Process attributes to print.
    :param dict kwargs: Filter configuration parameters.

    """

    # Name of the format produced by the formatter.
    fmt = ''

    # Configuration parameters with defaults.
    config = {}

    def __init__(self, stream, fields, **kwargs):
        self._stream = stream
        self.fields = fields

        unknown_keys = set(kwargs).difference(self.config)
        if unknown_keys:
            raise TypeError(
                'Unknown config parameters: {}'.format(
                    ', '.join(sorted(unknown_keys))))
        self._config = self.config.copy()
        self._config.update(kwargs)

    def _fields_values(self, process):
        """Return a list of fields values for a :class:`Process`."""
        return [process.get(field) for field in self.fields]

    def format(self, collection):
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

    def _format_process(self, process):
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

    def _write(self, data):
        if data is not None:
            self._stream.write(data)

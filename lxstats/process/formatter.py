"""Write field values for a collection of processes in a specific format."""


class Formatter:
    """Format a Process Collection.

    Parameters:
      stream: a file-like stream to write the formatted output to.
      fields: a list of Process attributes to print.
      Kwargs: filter configuration parameters.

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
        """Return a list of fields values for a L{Process}."""
        return [process.get(field) for field in self.fields]

    def format(self, collection):
        """Write the formatted output of the Collection."""
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
        """Format data for a Process.

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

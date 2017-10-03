"""Table formatter."""

from prettytable import PrettyTable

from ..formatter import Formatter


class TableFormatter(Formatter):
    """Format fields as a table.

    Config parameters:

    - borders: whether to print table borders
    """

    fmt = 'table'

    config = {'borders': False}

    def __init__(self, stream, fields, **kwargs):
        super().__init__(stream, fields, **kwargs)
        self._table = None

    def _format_header(self):
        self._table = PrettyTable()
        for field in self.fields:
            self._table.add_column(field, [], align='l')

    def _format_process(self, process):
        self._table.add_row(self._fields_values(process))

    def _dump(self):
        content = self._table.get_string(border=self._config['borders'])
        self._write(content + '\n')
        self._table = None

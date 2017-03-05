'''CSV formatter.'''

from csv import writer

from ..formatter import Formatter


class CSVFormatter(Formatter):
    '''Format fields in CSV.

    Config parameters:

    - tabs: use tabs as separators
    '''

    fmt = 'csv'

    config = {'tabs': False}

    def __init__(self, stream, fields, **kwargs):
        super().__init__(stream, fields, **kwargs)
        dialect = 'excel-tab' if self._config['tabs'] else 'excel'
        self._writer = writer(self._stream, dialect=dialect)

    def _format_header(self):
        self._writer.writerow(self.fields)

    def _format_process(self, process):
        self._writer.writerow(self._fields_values(process))

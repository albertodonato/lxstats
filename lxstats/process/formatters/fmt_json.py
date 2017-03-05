'''JSON formatter.'''

import json

from ..formatter import Formatter


class JSONFormatter(Formatter):
    '''Format fields in JSON.

    Config parameters:

      - indent: the amount of spaces for indentation (no indentation if None)
    '''

    fmt = 'json'

    config = {'indent': None}

    def __init__(self, stream, fields, **kwargs):
        super().__init__(stream, fields, **kwargs)
        self._data = {'fields': self.fields, 'processes': []}

    def _format_process(self, process):
        self._data['processes'].append(
            dict(zip(self.fields, self._fields_values(process))))

    def _dump(self):
        json.dump(self._data, self._stream, indent=self._config['indent'])

#
# This file is part of ProcSys.

# ProcSys is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# ProcSys is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ProcSys.  If not, see <http://www.gnu.org/licenses/>.

'''JSON formatter.'''

import json

from procsys.process.formatter import Formatter


class JSONFormatter(Formatter):
    '''Format fields in JSON.

    Config parameters:

      - indent: the amount of spaces for indentation (no indentation if None)
    '''

    fmt = 'json'

    config = {'indent': None}

    def __init__(self, stream, fields, **kwargs):
        super(JSONFormatter, self).__init__(stream, fields, **kwargs)
        self._data = {'fields': self.fields, 'processes': []}

    def _format_process(self, process):
        self._data['processes'].append(
            dict(zip(self.fields, self._fields_values(process))))

    def _dump(self):
        json.dump(self._data, self._stream, indent=self._config['indent'])

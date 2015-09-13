#
# This file is part of ProcSys.
#
# ProcSys is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# ProcSys is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ProcSys.  If not, see <http://www.gnu.org/licenses/>.

'''Table formatter.'''

from prettytable import PrettyTable

from ..formatter import Formatter


class TableFormatter(Formatter):
    '''Format fields as a table.

    Config parameters:

    - borders: whether to print table borders
    '''

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

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

'''CSV formatter.'''

from csv import writer

from procsys.process.formatter import Formatter


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

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

'''Formatter subclasses for different formats.'''

from procsys.process.formatters.fmt_csv import CSVFormatter
from procsys.process.formatters.fmt_json import JSONFormatter
from procsys.process.formatters.fmt_table import TableFormatter


_FORMATTERS = {
    formatter.fmt: formatter
    for formatter in (CSVFormatter, JSONFormatter, TableFormatter)}


def get_formats():
    '''Return a sorted list of available formatters names.'''
    return sorted(_FORMATTERS)


def get_formatter(name):
    '''Return the formatter class for the specified format.'''
    return _FORMATTERS[name]

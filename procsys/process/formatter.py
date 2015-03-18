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

'''Write field values for a collection of processes in a specific format.'''


class Formatter(object):
    '''Format a Process Collection.

    Parameters:
      stream: a file-like stream to write the formatted output to.
      fields: a list of Process attributes to print.
      Kwargs: filter configuration parameters.

    '''

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
        '''Return a list of fields values for a L{Process}.'''
        return [process.get(field) for field in self.fields]

    def format(self, collection):
        '''Write the formatted output of the Collection.'''
        self._format_header()
        for process in collection:
            self._format_process(process)
        self._format_footer()
        self._dump()

    def _format_header(self):
        '''Format the header.

        Subclasses can implement this.

        '''
        pass

    def _format_process(self, process):
        '''Format data for a Process.

        Subclasses can implement this.

        '''
        pass

    def _format_footer(self):
        '''Format footer.

        Subclasses can implement this.

        '''
        pass

    def _dump(self):
        '''Dump processed data to the stream.

        Subclasses can implement this.

        '''
        pass

    def _write(self, data):
        if data is not None:
            self._stream.write(data)

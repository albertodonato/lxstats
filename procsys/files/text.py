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

'''Classes for parsable text files.'''

from procsys.fs import File
from collections import Callable


class ParsedFile(File):
    '''A file whose content is parsed when read.

    Subclasses must implement the parser() method which receives the content of
    the file and returns the parsed information.
    '''

    def read(self):
        '''Read the file and preturn the parsed content.'''
        if not self.exists():
            return

        return self.parser(super().read())

    def parser(self, content):
        '''Parse the content of the file.

        Subclasses must implment this method to provide parsing.

        '''
        raise NotImplementedError('The parser method must be implemented.')


class SingleLineFile(ParsedFile):
    '''A single-line file that can be split into fields.

    The line is split into fields based on a separator (space by default).  If
    the separator is set to None, the stripped content of the file is returned.
    If separator is a callable, it's used to split the field (it gets passed
    the line and must return a list of fields).

    Subclasses can define a list of fields and a different separator.

    '''

    separator = ' '

    # If provided it must be a list of keys or (key, type) tuples. In the
    # latter case, the value is converted to the type. None can be used if the
    # field should not be parsed and included.
    fields = None

    def parser(self, content):
        # Take just fhe first line
        content = content.split('\n')[0]
        if self.separator is None:
            return content

        splitted = self._split(content)
        if self.fields is None:
            return splitted

        fields = self._get_fields()

        # Map fields values to their name converting to the proper type
        return {
            key: field_type(value)
            for (key, field_type), value in zip(fields, splitted)
            if key is not None}

    def _get_fields(self):
        fields = []
        for field in self.fields:
            if field is None:
                field = (None, None)
            elif isinstance(field, str):
                field = (field, str)

            fields.append(field)
        return fields

    def _split(self, content):
        if not content:
            return []

        if isinstance(self.separator, Callable):
            return self.separator(content)

        content = content.strip(self.separator)
        return content.split(self.separator)


class SplittedFile(ParsedFile):
    '''A file that is parsed by splitting the content in words.

    It's meant to work with files that have one word per line or a single
    space-separated line.

    '''

    def parser(self, content):
        lines = content.splitlines()
        if len(lines) == 1:
            return lines[0].split()
        else:
            return lines

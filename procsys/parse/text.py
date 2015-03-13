#
# This file is part of Procsys.

# Procsys is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Procsys is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Procsys.  If not, see <http://www.gnu.org/licenses/>.

'''Parser for text files.'''

import os
from itertools import izip


class FileParser(object):
    '''Parse a text file.'''

    def __init__(self, path):
        '''Parse a file.'''
        self.path = path

    def exists(self):
        '''Whether the file exists.'''
        return os.path.exists(self.path)

    def content(self):
        '''Return content of the file, or None if file doesn't exist.'''
        if not self.exists():
            return

        with open(self.path) as fd:
            return fd.read()

    def parse(self):
        '''Parse the content of the file.'''
        content = self.content()
        if content is None:
            return

        return self.parser(content.splitlines())

    def parser(self, lines):
        '''Parse the content of the file, provided as a list of lines.

        Subclasses must implment this method to provide parsing.
        '''
        raise NotImplementedError('The parser method must be implemented.')


class SingleLineFileParser(FileParser):
    '''Parse a single-line file into fields based on a common separator.

    Subclasses can define a list of fields and a different separator.

    '''

    separator = ' '

    # If provided it must be a list of keys or (key, type) tuples. In the
    # latter case, the value is converted to the type. None can be used if the
    # field should not be parsed and included.
    fields = None

    def parser(self, lines):
        content = lines[0]
        splitted = content.split(self.separator)
        if self.fields is None:
            return splitted

        fields = self._get_fields()

        # Map fields values to their name converting to the proper type
        return {
            key: field_type(value)
            for (key, field_type), value in izip(fields, splitted)
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


class SplitterFileParser(FileParser):
    '''Parse a file splitting the content in words.

    It's meant to work with files that have one word per line or a single
    space-separated line.

    '''

    def parser(self, lines):
        if len(lines) == 1:
            return lines[0].split()
        else:
            return lines

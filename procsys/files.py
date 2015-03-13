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

from collections import OrderedDict

from procsys.parse.text import FileParser, SplitterFileParser


class File(object):
    '''Wrapper to reaad/write a file.'''

    def __init__(self, path):
        self.path = path

    def read(self):
        '''Return file content.'''
        with open(self.path) as fh:
            return fh.read()

    def write(self, content):
        '''Write content to file.'''
        with open(self.path, 'w') as fh:
            fh.write(content)


class OptionsFile(File):
    '''File listing a set of options.'''

    def __init__(self, path):
        super(OptionsFile, self).__init__(path)
        self._parser = SplitterFileParser(path)

    @property
    def options(self):
        '''Return a list with avalilable options.'''
        return [self._strip_selected(value) for value in self._parse()]

    def _parse(self):
        return self._parser.parse()

    def _strip_selected(self, value):
        return value[1:-1] if value.startswith('[') else value


class SelectableOptionsFile(OptionsFile):
    '''File listing a set of options with a single selected one.'''

    @property
    def selected(self):
        '''Return the selected option.'''
        for value in self._parse():
            if value.startswith('['):
                return self._strip_selected(value)

    def select(self, value):
        '''Set the specified option value.

        ValueError is raised if the value is not valid.'''

        if value not in self.options:
            raise ValueError(value)
        self.write(value)


class TogglableOptionsFile(OptionsFile):
    '''A file with a list of options that can be individually enabled.

    Disabled options have names prefixed by "no".
    '''

    @property
    def options(self):
        '''Return a dict with options and their current values.'''
        options = OrderedDict()
        for option in super(TogglableOptionsFile, self).options:
            value = not option.startswith('no')
            if not value:
                option = option[2:]
            options[option] = value

        return options

    def toggle(self, option, value):
        '''Change the value of the specified option.'''
        if option not in self.options:
            raise ValueError(option)

        prefix = '' if value else 'no'
        self.write('{}{}'.format(prefix, option))


class ValueFile(File):
    '''File to read or set a value.'''

    def __init__(self, path):
        super(ValueFile, self).__init__(path)

    @property
    def value(self):
        '''Return the current value in the file.'''
        return self.read().strip()

    def set(self, value):
        self.write(value)


class ToggleFile(File):
    '''File to enable or disable an option.'''

    def __init__(self, path):
        super(ToggleFile, self).__init__(path)
        self._parser = FileParser(path)

    @property
    def enabled(self):
        '''Return whether the toggle value is enabled.'''
        return self._parser.content().strip() == '1'

    def toggle(self, value):
        '''Enable or disable the value.'''
        content = '1' if value else '0'
        self.write(content)

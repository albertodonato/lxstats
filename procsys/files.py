from procsys.parse.text import SingleLineFileParser


class ToggleFile(object):
    '''Read/set options for a toggle-like file.'''

    def __init__(self, path):
        self.path = path

    @property
    def options(self):
        '''Return a list with avalilable options.'''
        return [self._strip_selected(value) for value in self._parse()]

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
        with open(self.path, 'w') as fh:
            fh.write(value)

    def _parse(self):
        parser = SingleLineFileParser(self.path)
        return parser.parse()

    def _strip_selected(self, value):
        return value[1:-1] if value.startswith('[') else value

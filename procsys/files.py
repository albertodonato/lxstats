from procsys.parse.text import FileParser, SplitterFileParser


class OptionsFile(object):
    '''File listing a set of options.'''

    def __init__(self, path):
        self.path = path
        self._parser = SplitterFileParser(self.path)

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
        with open(self.path, 'w') as fh:
            fh.write(value)


class ToggleFile(object):
    '''File to enable or disable an option.'''

    def __init__(self, path):
        self.path = path
        self._parser = FileParser(self.path)

    @property
    def enabled(self):
        '''Return whether the toggle value is enabled.'''
        return self._parser.content().strip() == '1'

    def toggle(self, value):
        '''Enable or disable the value.'''
        content = '1' if value else '0'
        with open(self.path, 'w') as fh:
            fh.write(content)

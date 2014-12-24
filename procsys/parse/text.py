'''Parser for text files.'''

import os


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
    # latter case, the value is converted to the type.
    fields = None

    def parser(self, lines):
        content = lines[0]
        splitted = content.split(self.separator)
        if self.fields is None:
            return splitted

        fields = self._get_fields()

        result = {}
        for idx, (key, field_type) in enumerate(fields):
            result[key] = field_type(splitted[idx])

        return result

    def _get_fields(self):
        fields = []
        for field in self.fields:
            if isinstance(field, str):
                field = (field, str)

            fields.append(field)
        return fields

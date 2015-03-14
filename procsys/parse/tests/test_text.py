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

from procsys.testing import TestCase

from procsys.parse.text import (
    FileParser, SingleLineFileParser, SplitterFileParser)


class FileParserTests(TestCase):

    def test_path(self):
        '''The FileParser stores the specified path.'''
        parser = FileParser('/foo/bar')
        self.assertEqual(parser.path, '/foo/bar')

    def test_exists_true(self):
        '''FileParser.exists returns True if the file exists.'''
        path = self.mkfile()
        parser = FileParser(path)
        self.assertTrue(parser.exists())

    def test_exists_false(self):
        '''FileParser.exists returns False if the file doesn't exists.'''
        path = self.mktemp()
        parser = FileParser(path)
        self.assertFalse(parser.exists())

    def test_content(self):
        '''FileParser.content returns the content of the file.'''
        path = self.mkfile(content='some content')
        parser = FileParser(path)
        self.assertEqual(parser.content(), 'some content')

    def test_content_not_existent(self):
        '''FileParser.content returns None if the file doesn't exist.'''
        path = self.mktemp()
        parser = FileParser(path)
        self.assertIsNone(parser.content())

    def test_parse(self):
        '''FileParser.parse calls the parser with a list of content lines.'''
        path = self.mkfile(content='line 1\nline 2')
        parser = FileParser(path)
        parser.parser = lambda lines: [line + ' parsed' for line in lines]
        self.assertEqual(parser.parse(), ['line 1 parsed', 'line 2 parsed'])

    def test_parse_not_existent(self):
        '''FileParser.parse returns None if file doesn't exist.'''
        path = self.mktemp()
        parser = FileParser(path)
        parser.parser = lambda lines: 'called'
        # The parser method is not called
        self.assertIsNone(parser.parse())


class SingleLineFileParserTests(TestCase):

    def test_default_parser(self):
        '''By default the file content is split on spaces.'''
        path = self.mkfile(content='foo bar baz')
        parser = SingleLineFileParser(path)
        self.assertEqual(parser.parse(), ['foo', 'bar', 'baz'])

    def test_parser_different_separator(self):
        '''The file content is split on a custom separator.'''
        path = self.mkfile(content='foo|bar|baz')
        parser = SingleLineFileParser(path)
        parser.separator = "|"
        self.assertEqual(parser.parse(), ['foo', 'bar', 'baz'])

    def test_parser_with_fields(self):
        '''If fields are specified, the parser returns a dict.'''
        path = self.mkfile(content='foo bar baz')
        parser = SingleLineFileParser(path)
        parser.fields = ('one', 'two', 'three')
        self.assertEqual(
            parser.parse(), {'one': 'foo', 'two': 'bar', 'three': 'baz'})

    def test_parser_with_fields_with_type(self):
        '''If fields are specified, the parser returns a dict.'''
        path = self.mkfile(content='foo 1 30.3')
        parser = SingleLineFileParser(path)
        parser.fields = ('one', ('two', int), ('three', float))
        self.assertEqual(
            parser.parse(), {'one': 'foo', 'two': 1, 'three': 30.3})

    def test_parser_with_fields_with_none(self):
        '''If a field is None, it's skipped in the result.'''
        path = self.mkfile(content='foo baz bar')
        parser = SingleLineFileParser(path)
        parser.fields = ('one', None, 'three')
        self.assertEqual(parser.parse(), {'one': 'foo', 'three': 'bar'})

    def test_parser_with_less_fields(self):
        '''If fields less fields are present, they're skipped in the result.'''
        path = self.mkfile(content='foo bar')
        parser = SingleLineFileParser(path)
        parser.fields = ('one', 'two', 'three', 'four')
        self.assertEqual(parser.parse(), {'one': 'foo', 'two': 'bar'})


class SplitterFileParserTests(TestCase):

    def test_parser_single_line(self):
        '''A single line of content is split on spaces.'''
        path = self.mkfile(content='foo bar baz')
        parser = SplitterFileParser(path)
        self.assertEqual(parser.parse(), ['foo', 'bar', 'baz'])

    def test_parser_multiple_lines(self):
        '''A file with multiple lines is split on newlines.'''
        path = self.mkfile(content='foo\nbar\nbaz')
        parser = SplitterFileParser(path)
        self.assertEqual(parser.parse(), ['foo', 'bar', 'baz'])

    def test_parser_multiple_lines_trailing_newline(self):
        '''Trailing newline is ignored.'''
        path = self.mkfile(content='foo\nbar\nbaz\n')
        parser = SplitterFileParser(path)
        self.assertEqual(parser.parse(), ['foo', 'bar', 'baz'])

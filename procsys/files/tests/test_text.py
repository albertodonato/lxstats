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

from procsys.files.text import ParsedFile, SingleLineFile, SplittedFile


class ParsedFileTests(TestCase):

    def test_parse(self):
        '''ParsedFile.parse calls the parser with the file content.'''
        content = 'line 1\nline 2'
        path = self.mkfile(content=content)
        parser = ParsedFile(path)
        parser.parser = lambda content: content
        self.assertEqual(parser.parse(), content)

    def test_parse_not_existent(self):
        '''FileParser.parse returns None if file doesn't exist.'''
        path = self.mktemp()
        parser = ParsedFile(path)
        parser.parser = lambda content: content
        # The parser method is not called
        self.assertIsNone(parser.parse())


class SingleLineFileTests(TestCase):

    def test_default_parser(self):
        '''By default the file content is split on spaces.'''
        path = self.mkfile(content='foo bar baz')
        parser = SingleLineFile(path)
        self.assertEqual(parser.parse(), ['foo', 'bar', 'baz'])

    def test_parser_different_separator(self):
        '''The file content is split on a custom separator.'''
        path = self.mkfile(content='foo|bar|baz')
        parser = SingleLineFile(path)
        parser.separator = "|"
        self.assertEqual(parser.parse(), ['foo', 'bar', 'baz'])

    def test_parser_with_fields(self):
        '''If fields are specified, the parser returns a dict.'''
        path = self.mkfile(content='foo bar baz')
        parser = SingleLineFile(path)
        parser.fields = ('one', 'two', 'three')
        self.assertEqual(
            parser.parse(), {'one': 'foo', 'two': 'bar', 'three': 'baz'})

    def test_parser_with_fields_with_type(self):
        '''If fields are specified, the parser returns a dict.'''
        path = self.mkfile(content='foo 1 30.3')
        parser = SingleLineFile(path)
        parser.fields = ('one', ('two', int), ('three', float))
        self.assertEqual(
            parser.parse(), {'one': 'foo', 'two': 1, 'three': 30.3})

    def test_parser_with_fields_with_none(self):
        '''If a field is None, it's skipped in the result.'''
        path = self.mkfile(content='foo baz bar')
        parser = SingleLineFile(path)
        parser.fields = ('one', None, 'three')
        self.assertEqual(parser.parse(), {'one': 'foo', 'three': 'bar'})

    def test_parser_with_less_fields(self):
        '''If fields less fields are present, they're skipped in the result.'''
        path = self.mkfile(content='foo bar')
        parser = SingleLineFile(path)
        parser.fields = ('one', 'two', 'three', 'four')
        self.assertEqual(parser.parse(), {'one': 'foo', 'two': 'bar'})


class SplittedFileTests(TestCase):

    def test_parser_single_line(self):
        '''A single line of content is split on spaces.'''
        path = self.mkfile(content='foo bar baz')
        parser = SplittedFile(path)
        self.assertEqual(parser.parse(), ['foo', 'bar', 'baz'])

    def test_parser_multiple_lines(self):
        '''A file with multiple lines is split on newlines.'''
        path = self.mkfile(content='foo\nbar\nbaz')
        parser = SplittedFile(path)
        self.assertEqual(parser.parse(), ['foo', 'bar', 'baz'])

    def test_parser_multiple_lines_trailing_newline(self):
        '''Trailing newline is ignored.'''
        path = self.mkfile(content='foo\nbar\nbaz\n')
        parser = SplittedFile(path)
        self.assertEqual(parser.parse(), ['foo', 'bar', 'baz'])

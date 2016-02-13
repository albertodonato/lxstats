#
# This file is part of LxStats.
#
# LxStats is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# LxStats is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# LxStats.  If not, see <http://www.gnu.org/licenses/>.

from ...testing import TestCase
from ..text import ParsedFile, SingleLineFile, SplittedFile


class ParsedFileTests(TestCase):

    def test_parse(self):
        '''ParsedFile.parse calls the parser with the file content.'''
        content = 'line 1\nline 2'
        path = self.tempdir.mkfile(content=content)
        parsed_file = ParsedFile(path)
        parsed_file._parse = lambda content: content
        self.assertEqual(parsed_file.parse(), content)

    def test_parse_not_existent(self):
        '''FileParser.parse returns None if file doesn't exist.'''
        path = self.tempdir.join('file')
        parsed_file = ParsedFile(path)
        # The parser method is not called
        self.assertIsNone(parsed_file.parse())


class SingleLineFileTests(TestCase):

    def test_parse_empty_file(self):
        '''If the file is empty, an empty list is returned.'''
        path = self.tempdir.mkfile()
        single_line_file = SingleLineFile(path)
        self.assertEqual(single_line_file.parse(), [])

    def test_parse_empty_file_with_fields(self):
        '''If the file is empty and fields are set, return an empty dict.'''
        path = self.tempdir.mkfile()
        single_line_file = SingleLineFile(path)
        single_line_file.fields = ('foo', 'bar')
        self.assertEqual(single_line_file.parse(), {})

    def test_parse_only_first_line(self):
        '''Only the first line of the file is parsed.'''
        path = self.tempdir.mkfile(content='foo\nbar\nbaz\n')
        single_line_file = SingleLineFile(path)
        self.assertEqual(single_line_file.parse(), ['foo'])

    def test_parse_default_separator(self):
        '''By default the file content is split on spaces.'''
        path = self.tempdir.mkfile(content='foo bar baz')
        single_line_file = SingleLineFile(path)
        self.assertEqual(single_line_file.parse(), ['foo', 'bar', 'baz'])

    def test_parse_different_separator(self):
        '''The file content is split on a custom separator.'''
        path = self.tempdir.mkfile(content='foo|bar|baz')
        single_line_file = SingleLineFile(path)
        single_line_file.separator = '|'
        self.assertEqual(single_line_file.parse(), ['foo', 'bar', 'baz'])

    def test_parse_no_separator(self):
        '''If no separator is set, the stripped content is returned.'''
        path = self.tempdir.mkfile(content='just some text\n')
        single_line_file = SingleLineFile(path)
        single_line_file.separator = None
        self.assertEqual(single_line_file.parse(), 'just some text')

    def test_parse_with_fields(self):
        '''If fields are specified, a dict is returned upon parsing.'''
        path = self.tempdir.mkfile(content='foo bar baz')
        single_line_file = SingleLineFile(path)
        single_line_file.fields = ('one', 'two', 'three')
        self.assertEqual(
            single_line_file.parse(),
            {'one': 'foo', 'two': 'bar', 'three': 'baz'})

    def test_parse_with_fields_with_type(self):
        '''Typed fields are converted in the result.'''
        path = self.tempdir.mkfile(content='foo 1 30.3')
        single_line_file = SingleLineFile(path)
        single_line_file.fields = ('one', ('two', int), ('three', float))
        self.assertEqual(
            single_line_file.parse(), {'one': 'foo', 'two': 1, 'three': 30.3})

    def test_parse_with_fields_with_none(self):
        '''If a field is None, it's skipped in the result.'''
        path = self.tempdir.mkfile(content='foo baz bar')
        single_line_file = SingleLineFile(path)
        single_line_file.fields = ('one', None, 'three')
        self.assertEqual(
            single_line_file.parse(), {'one': 'foo', 'three': 'bar'})

    def test_parse_with_less_fields(self):
        '''If fields less fields are present, they're skipped in the result.'''
        path = self.tempdir.mkfile(content='foo bar')
        single_line_file = SingleLineFile(path)
        single_line_file.fields = ('one', 'two', 'three', 'four')
        self.assertEqual(
            single_line_file.parse(), {'one': 'foo', 'two': 'bar'})


class SplittedFileTests(TestCase):

    def test_parse_single_line(self):
        '''A single line of content is split on spaces.'''
        path = self.tempdir.mkfile(content='foo bar baz')
        splitted_file = SplittedFile(path)
        self.assertEqual(splitted_file.parse(), ['foo', 'bar', 'baz'])

    def test_parse_multiple_lines(self):
        '''A file with multiple lines is split on newlines.'''
        path = self.tempdir.mkfile(content='foo\nbar\nbaz')
        splitted_file = SplittedFile(path)
        self.assertEqual(splitted_file.parse(), ['foo', 'bar', 'baz'])

    def test_parse_multiple_lines_trailing_newline(self):
        '''Trailing newline is ignored.'''
        path = self.tempdir.mkfile(content='foo\nbar\nbaz\n')
        splitted_file = SplittedFile(path)
        self.assertEqual(splitted_file.parse(), ['foo', 'bar', 'baz'])

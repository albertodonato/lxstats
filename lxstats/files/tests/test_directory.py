from ..directory import ParsedDirectory
from ...testing import TestCase


class SampleParsedDirectory(ParsedDirectory):

    def _parse(self, path):
        return path.name + '-parsed'


class ParsedDirectoryTests(TestCase):

    def test_parse(self):
        """ParsedDirectory.parse calls the parser with path of each file."""
        self.tempdir.mkfile(path='foo')
        self.tempdir.mkfile(path='bar')
        parsed_dir = SampleParsedDirectory(self.tempdir.path)
        self.assertEqual(
            parsed_dir.parse(), {'foo': 'foo-parsed', 'bar': 'bar-parsed'})

    def test_parse_not_existent(self):
        """ParsedDirectory.parse returns None if directory doesn't exist."""
        parsed_dir = SampleParsedDirectory(self.tempdir.join('somedir'))
        self.assertIsNone(parsed_dir.parse())

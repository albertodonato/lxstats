import pytest

from lxstats.files.text import (
    ParsedFile,
    SingleLineFile,
    SplittedFile,
)


class SampleParsedFile(ParsedFile):
    def _parse(self, content):
        return f"parsed {content}"


class TestParsedFile:
    def test_parse(self, tmpfile):
        """ParsedFile.parse calls the parser with the file content."""
        content = "line 1\nline 2"
        tmpfile.write_text(content)
        parsed_file = SampleParsedFile(tmpfile)
        assert parsed_file.parse() == f"parsed {content}"

    def test_parse_not_existent(self, tmpfile):
        """ParsedFile.parse returns None if file doesn't exist."""
        parsed_file = SampleParsedFile(tmpfile)
        assert parsed_file.parse() is None


@pytest.fixture
def single_line_file(tmpfile):
    yield SingleLineFile(tmpfile)


class TestSingleLineFile:
    def test_parse_empty_file(self, single_line_file, tmpfile):
        """If the file is empty, an empty list is returned."""
        tmpfile.touch()
        assert single_line_file.parse() == []

    def test_parse_empty_file_with_fields(self, single_line_file, tmpfile):
        """If the file is empty and fields are set, return an empty dict."""
        tmpfile.touch()
        single_line_file.fields = ("foo", "bar")
        assert single_line_file.parse() == {}

    def test_parse_only_first_line(self, single_line_file, tmpfile):
        """Only the first line of the file is parsed."""
        tmpfile.write_text("foo\nbar\nbaz\n")
        assert single_line_file.parse() == ["foo"]

    def test_parse_default_separator(self, single_line_file, tmpfile):
        """By default the file content is split on spaces."""
        tmpfile.write_text("foo bar baz")
        assert single_line_file.parse() == ["foo", "bar", "baz"]

    def test_parse_different_separator(self, single_line_file, tmpfile):
        """The file content is split on a custom separator."""
        tmpfile.write_text("foo|bar|baz")
        single_line_file.separator = "|"
        assert single_line_file.parse() == ["foo", "bar", "baz"]

    def test_parse_no_separator(self, single_line_file, tmpfile):
        """If no separator is set, the stripped content is returned."""
        tmpfile.write_text("just some text\n")
        single_line_file.separator = None
        assert single_line_file.parse() == "just some text"

    def test_parse_separator_callable(self, single_line_file, tmpfile):
        tmpfile.write_text("foo bar baz")
        single_line_file.separator = lambda content: [
            f"x-{line}" for line in content.split()
        ]
        assert single_line_file.parse() == ["x-foo", "x-bar", "x-baz"]

    @pytest.mark.parametrize(
        "fields,content,parsed",
        [
            (
                ("one", "two", "three"),
                "foo bar baz",
                {"one": "foo", "two": "bar", "three": "baz"},
            ),
            # with fields type
            (
                ("one", ("two", int), ("three", float)),
                "foo 1 30.3",
                {"one": "foo", "two": 1, "three": 30.3},
            ),
            # with skipped field
            (
                ("one", None, "three"),
                "foo bar baz",
                {"one": "foo", "three": "baz"},
            ),
            # with less fields than available
            (
                ("one", "two", "three", "four"),
                "foo bar",
                {"one": "foo", "two": "bar"},
            ),
        ],
    )
    def test_parse_with_fields(
        self, single_line_file, tmpfile, fields, content, parsed
    ):
        """If fields are specified, a dict is returned upon parsing."""
        tmpfile.write_text(content)
        single_line_file.fields = fields
        assert single_line_file.parse() == parsed


class TestSplittedFile:
    @pytest.mark.parametrize(
        "content",
        [
            "foo bar baz",  # single line with spaces
            "foo\nbar\nbaz",  # multiple lines
            "foo\nbar\nbaz\n",  # trailing newline is stripped
        ],
    )
    def test_parse(self, tmpfile, content):
        """File content is split based on separateor."""
        tmpfile.write_text(content)
        splitted_file = SplittedFile(tmpfile)
        assert splitted_file.parse() == ["foo", "bar", "baz"]

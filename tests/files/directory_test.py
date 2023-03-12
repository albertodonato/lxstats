from lxstats.files.directory import ParsedDirectory


class SampleParsedDirectory(ParsedDirectory):
    def _parse(self, path):
        return path.name + "-parsed"


class TestParsedDirectory:
    def test_parse(self, tmpdir):
        """ParsedDirectory.parse calls the parser with path of each file."""
        (tmpdir / "foo").write_text("", "utf-8")
        (tmpdir / "bar").write_text("", "utf-8")
        parsed_dir = SampleParsedDirectory(tmpdir)
        assert parsed_dir.parse() == {"foo": "foo-parsed", "bar": "bar-parsed"}

    def test_parse_not_existent(self, tmpdir):
        """ParsedDirectory.parse returns None if directory doesn't exist."""
        parsed_dir = SampleParsedDirectory(tmpdir / "somedir")
        assert parsed_dir.parse() is None

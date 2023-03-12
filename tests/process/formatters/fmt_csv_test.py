from io import StringIO

from lxstats.process.formatters import CSVFormatter


class TestCSVFormatter:
    def test_format(self, collection):
        """CSVFormatter outputs CSV file with processes data."""
        stream = StringIO()
        formatter = CSVFormatter(stream, ["pid", "cmd"])
        formatter.format(collection)
        assert stream.getvalue() == (
            "pid,cmd\r\n" "10,/bin/foo\r\n" "20,/bin/bar\r\n"
        )

    def test_format_tabs(self, collection):
        """CSVFormatter can use tabs as field separators."""
        stream = StringIO()
        formatter = CSVFormatter(stream, ["pid", "cmd"], tabs=True)
        formatter.format(collection)
        assert stream.getvalue() == (
            "pid\tcmd\r\n" "10\t/bin/foo\r\n" "20\t/bin/bar\r\n"
        )

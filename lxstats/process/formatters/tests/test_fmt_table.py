from io import StringIO

from .. import TableFormatter


class TestTableFormatter:
    def test_format(self, collection):
        """TableFormatter outputs a table with processes data."""
        stream = StringIO()
        formatter = TableFormatter(stream, ["pid", "cmd"])
        formatter.format(collection)
        assert stream.getvalue() == (
            " pid  cmd      \n" " 10   /bin/foo \n" " 20   /bin/bar \n"
        )

    def test_format_border(self, collection):
        """TableFormatter can add borders to the table."""
        stream = StringIO()
        formatter = TableFormatter(stream, ["pid", "cmd"], borders=True)
        formatter.format(collection)
        assert stream.getvalue() == (
            "+-----+----------+\n"
            "| pid | cmd      |\n"
            "+-----+----------+\n"
            "| 10  | /bin/foo |\n"
            "| 20  | /bin/bar |\n"
            "+-----+----------+\n"
        )

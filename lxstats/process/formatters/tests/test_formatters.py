from .. import (
    get_formats,
    get_formatter,
)
from ..fmt_table import TableFormatter


class TestGetFormats:
    def test_get_formats(self):
        """get_formats return a sorted list of formatters."""
        assert get_formats() == ["csv", "json", "table"]


class TestGetFormatter:
    def test_get_formatter(self):
        """get_formatter return a formatter by name."""
        assert get_formatter("table") == TableFormatter

"""Formatter subclasses for different formats."""

from .fmt_csv import CSVFormatter
from .fmt_json import JSONFormatter
from .fmt_table import TableFormatter


_FORMATTERS = {
    formatter.fmt: formatter
    for formatter in (CSVFormatter, JSONFormatter, TableFormatter)}


def get_formats():
    """Return a sorted list of available formatters names."""
    return sorted(_FORMATTERS)


def get_formatter(name):
    """Return the formatter class for the specified format."""
    return _FORMATTERS[name]

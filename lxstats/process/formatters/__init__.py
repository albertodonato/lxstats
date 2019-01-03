"""Formatter subclasses for different formats."""

from typing import (
    Dict,
    List,
    Type,
)

from ..formatter import Formatter
from .fmt_csv import CSVFormatter
from .fmt_json import JSONFormatter
from .fmt_table import TableFormatter

_FORMATTERS: Dict[str, Type[Formatter]] = {
    formatter.fmt: formatter
    for formatter in (CSVFormatter, JSONFormatter, TableFormatter)
}


def get_formats() -> List[str]:
    """Return a sorted list of available formatters names."""
    return sorted(_FORMATTERS)


def get_formatter(name: str) -> Type[Formatter]:
    """Return the formatter class for the specified format."""
    return _FORMATTERS[name]

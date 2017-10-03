from unittest import TestCase

from .. import get_formats, get_formatter
from ..fmt_table import TableFormatter


class GetFormatsTest(TestCase):

    def test_get_formats(self):
        """get_formats return a sorted list of formatters."""
        self.assertEqual(get_formats(), ['csv', 'json', 'table'])


class GetFormatterTest(TestCase):

    def test_get_formatter(self):
        """get_formatter return a formatter by name."""
        self.assertIs(get_formatter('table'), TableFormatter)

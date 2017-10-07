from io import StringIO

from ....testing import TestCase
from .. import CSVFormatter
from ...collection import (
    Collector,
    Collection)


class CSVFormatterTests(TestCase):

    def setUp(self):
        super().setUp()
        self.stream = StringIO()
        collector = Collector(proc=self.tempdir.path, pids=(10, 20))
        self.collection = Collection(collector=collector)
        self.make_process_file(10, 'cmdline', content='/bin/foo')
        self.make_process_file(20, 'cmdline', content='/bin/bar')

    def test_format(self):
        """CSVFormatter outputs CSV file with processes data."""
        formatter = CSVFormatter(self.stream, ['pid', 'cmd'])
        formatter.format(self.collection)
        self.assertEqual(
            self.stream.getvalue(),
            'pid,cmd\r\n'
            '10,/bin/foo\r\n'
            '20,/bin/bar\r\n')

    def test_format_tabs(self):
        """CSVFormatter can use tabs as field separators."""
        formatter = CSVFormatter(self.stream, ['pid', 'cmd'], tabs=True)
        formatter.format(self.collection)
        self.assertEqual(
            self.stream.getvalue(),
            'pid\tcmd\r\n'
            '10\t/bin/foo\r\n'
            '20\t/bin/bar\r\n')

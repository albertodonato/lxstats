from io import StringIO

from ....testing import TestCase
from .. import TableFormatter
from ...collection import Collector, Collection


class TableFormatterTests(TestCase):

    def setUp(self):
        super().setUp()
        self.stream = StringIO()
        collector = Collector(proc=self.tempdir.path, pids=(10, 20))
        self.collection = Collection(collector=collector)
        self.make_process_file(10, 'cmdline', content='/bin/foo')
        self.make_process_file(20, 'cmdline', content='/bin/bar')

    def test_format(self):
        """TableFormatter outputs a table with processes data."""
        formatter = TableFormatter(self.stream, ['pid', 'cmd'])
        formatter.format(self.collection)
        self.assertEqual(
            self.stream.getvalue(),
            ' pid  cmd      \n'
            ' 10   /bin/foo \n'
            ' 20   /bin/bar \n')

    def test_format_border(self):
        """TableFormatter can add borders to the table."""
        formatter = TableFormatter(
            self.stream, ['pid', 'cmd'], borders=True)
        formatter.format(self.collection)
        self.assertEqual(
            self.stream.getvalue(),
            '+-----+----------+\n'
            '| pid | cmd      |\n'
            '+-----+----------+\n'
            '| 10  | /bin/foo |\n'
            '| 20  | /bin/bar |\n'
            '+-----+----------+\n')

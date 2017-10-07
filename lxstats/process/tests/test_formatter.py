from io import StringIO

from ...testing import TestCase

from ..formatter import Formatter
from ..collection import (
    Collection,
    Collector)
from ..process import Process


class SampleFormatter(Formatter):

    config = {'option': 10}
    endl = '\n'

    def _format_header(self):
        self._write('header\n')

    def _format_footer(self):
        self._write('footer\n')

    def _format_process(self, process):
        self._write('process {} {}\n'.format(process.pid, process.cmd))

    def _dump(self):
        self._write('dump\n')


class FormatterTests(TestCase):

    def setUp(self):
        super().setUp()
        self.stream = StringIO()

    def test_format_no_op_default(self):
        """By default, format methods don't output anything."""
        self.make_process_file(10, 'cmdline', content='cmd1')
        self.make_process_file(20, 'cmdline', content='cmd2')
        collector = Collector(proc=self.tempdir.path, pids=(10, 20))
        collection = Collection(collector=collector)
        formatter = Formatter(self.stream, ['pid'])
        formatter.format(collection)
        self.assertEqual(self.stream.getvalue(), '')

    def test_format(self):
        """Formatter.format outputs process info with header and footer."""
        self.make_process_file(10, 'cmdline', content='cmd1')
        self.make_process_file(20, 'cmdline', content='cmd2')
        collector = Collector(proc=self.tempdir.path, pids=(10, 20))
        collection = Collection(collector=collector)
        formatter = SampleFormatter(self.stream, ['pid', 'cmd'])
        formatter.format(collection)
        self.assertEqual(
            self.stream.getvalue(),
            'header\n'
            'process 10 cmd1\n'
            'process 20 cmd2\n'
            'footer\n'
            'dump\n')

    def test_fields_values(self):
        """Formatter._fields_values returns a list with Process values."""
        self.make_process_file(10, 'cmdline', '/bin/foo')
        formatter = SampleFormatter(self.stream, ['pid', 'cmd'])
        process = Process(10, proc_dir='{}/10'.format(self.tempdir.path))
        process.collect_stats()
        self.assertEqual(
            formatter._fields_values(process), [10, '/bin/foo'])

    def test_config_default_value(self):
        """Formatter can have config options with default values."""
        formatter = SampleFormatter(self.stream, ['pid', 'cmdline'])
        self.assertEqual(formatter._config, {'option': 10})

    def test_config_set_value(self):
        """It's possible to specify config options to Formatter."""
        formatter = SampleFormatter(self.stream, ['pid', 'cmdline'], option=30)
        self.assertEqual(formatter._config, {'option': 30})

    def test_unknown_option(self):
        """If an unknown option is specified, an error is raised."""
        self.assertRaises(
            TypeError, SampleFormatter, self.stream, ['pid', 'cmdline'],
            unknown_option=30)

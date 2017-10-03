from ...testing import TestCase
from ..process import Process
from ..filter import CommandLineFilter


class CommandLineFilterTests(TestCase):

    def setUp(self):
        super().setUp()
        self.pid = 10
        self.process = Process(
            self.pid, proc_dir='{}/{}'.format(self.tempdir.path, self.pid))

    def test_filter_matching_process(self):
        """CommandLineFilter matches a process."""
        proc_filter = CommandLineFilter('foo')
        self.make_process_file(
            self.pid, 'cmdline', content='/bin/foo\x00bar\x00')
        self.process.collect_stats()
        self.assertTrue(proc_filter(self.process))

    def test_filter_non_matching_process(self):
        """CommandLineFilter doesn't match a process."""
        proc_filter = CommandLineFilter('foo')
        self.make_process_file(
            self.pid, 'cmdline', content='/bin/bar\x00foo\x00')
        self.process.collect_stats()
        self.assertFalse(proc_filter(self.process))

    def test_include_args(self):
        """Arguments are included in match if include_args is True."""
        proc_filter = CommandLineFilter('foo', include_args=True)
        self.make_process_file(
            self.pid, 'cmdline', content='/bin/bar\x00foo\x00')
        self.process.collect_stats()
        self.assertTrue(proc_filter(self.process))

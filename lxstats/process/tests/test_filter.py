from ...testing import TestCase
from ..process import Process
from ..filter import (
    CommandNameFilter,
    CommandLineFilter)


class CommandNameFilterTests(TestCase):

    def setUp(self):
        super().setUp()
        self.pid = 10
        self.process = Process(
            self.pid, proc_dir='{}/{}'.format(self.tempdir.path, self.pid))

    def test_filter_matching_command(self):
        """CommandNameFilter matches a process."""
        proc_filter = CommandNameFilter('foo')
        self.make_process_file(
            self.pid, 'cmdline', content='foo\x00bar\x00')
        self.process.collect_stats()
        self.assertTrue(proc_filter(self.process))

    def test_filter_only_exact(self):
        """CommandNameFilter only matches exact command names."""
        proc_filter = CommandNameFilter('foo')
        self.make_process_file(
            self.pid, 'cmdline', content='/bin/foo\x00')
        self.process.collect_stats()
        self.assertFalse(proc_filter(self.process))

    def test_filter_matching_comm(self):
        """CommandNameFilter matches a process by comm value."""
        proc_filter = CommandNameFilter('foo')
        self.make_process_file(self.pid, 'comm', content='foo')
        self.process.collect_stats()
        self.assertTrue(proc_filter(self.process))


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

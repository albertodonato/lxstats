from pathlib import Path

from ..process import Process
from ..collection import (
    Collector,
    Collection)
from ...testing import TestCase


class CollectorTests(TestCase):

    def test_collector_scan(self):
        """The Collector returns Processes for all PIDs."""
        self.make_process_file(10, 'cmdline')
        self.make_process_file(20, 'cmdline')
        self.make_process_file(30, 'cmdline')
        collector = Collector(proc=self.tempdir.path)
        self.assertCountEqual(
            (process.pid for process in collector.collect()),
            [10, 20, 30])

    def test_collector_with_pids(self):
        """If PIDs are provided, only those are included."""
        self.make_process_file(10, 'cmdline')
        self.make_process_file(20, 'cmdline')
        self.make_process_file(30, 'cmdline')
        collector = Collector(proc=self.tempdir.path, pids=(10, 30))
        self.assertCountEqual(
            (process.pid for process in collector.collect()),
            [10, 30])

    def test_collector_with_pids_sorts(self):
        """Processes are listed in PID order."""
        self.make_process_file(10, 'cmdline')
        self.make_process_file(20, 'cmdline')
        collector = Collector(proc=self.tempdir.path, pids=(20, 10))
        self.assertCountEqual(
            (process.pid for process in collector.collect()),
            [10, 20])

    def test_collector_skip_non_existing(self):
        """Collector skips non-existing processes."""
        self.make_process_file(10, 'cmdline')
        collector = Collector(proc=self.tempdir.path, pids=(10, 20))
        self.assertEqual(
            [process.pid for process in collector.collect()], [10])


class CollectionTests(TestCase):

    def setUp(self):
        super().setUp()
        pids = (10, 30, 20)  # Not ordered so tests can sort
        self.collector = Collector(proc=self.tempdir.path, pids=pids)
        self.make_process_file(10, 'comm', content='foo')
        self.make_process_file(20, 'comm', content='zza')
        self.make_process_file(30, 'comm', content='bar')

    def process_list(self, pids):
        """Return a list of processes with specified pids."""
        return [
            Process(pid, self.tempdir.path / str(pid))
            for pid in pids]

    def test_default_collector(self):
        """If a collector is not specified, one that looks at /proc is set."""
        collection = Collection()
        self.assertEqual(collection._collector._proc, Path('/proc'))

    def test_iter(self):
        """Collector is an iterable yielding Processes."""
        collection = Collection(collector=self.collector)
        self.assertCountEqual(collection, self.process_list([10, 20, 30]))

    def test_sort_by(self):
        """Collector can sort by the specified Process stat."""
        collection = Collection(collector=self.collector, sort_by='comm')
        self.assertEqual(list(collection), self.process_list([30, 10, 20]))

    def test_sort_by_reversed(self):
        """Collector can sort in reverse order."""
        collection = Collection(collector=self.collector, sort_by='-comm')
        self.assertEqual(list(collection), self.process_list([20, 10, 30]))

    def test_add_filter(self):
        """Collector.add_filter adds a filter for processes."""
        collection = Collection(collector=self.collector)
        collection.add_filter(lambda proc: proc.pid != 20)
        self.assertCountEqual(collection, self.process_list([10, 30]))

    def test_filter_multiple(self):
        """Multiple filters can be added."""
        collection = Collection(collector=self.collector)
        collection.add_filter(lambda proc: proc.pid != 20)
        collection.add_filter(lambda proc: proc.pid != 30)
        self.assertCountEqual(collection, self.process_list([10]))

    def test_filter_exclusive(self):
        """Filters are applied in 'or'."""
        collection = Collection(collector=self.collector)
        collection.add_filter(lambda proc: proc.pid == 10)
        collection.add_filter(lambda proc: proc.pid != 10)
        self.assertCountEqual(collection, [])

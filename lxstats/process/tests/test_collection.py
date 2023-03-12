from pathlib import Path
import random

import pytest

from ..collection import (
    Collection,
    Collector,
)
from ..process import Process


@pytest.fixture
def pids():
    yield [10, 20, 30]


@pytest.fixture
def processes_cmdline(pids, make_process_dir):
    for pid in pids:
        (make_process_dir(pid) / "cmdline").touch()


@pytest.mark.usefixtures("processes_cmdline")
class TestCollector:
    def test_collector_scan(self, proc_dir, pids):
        """The Collector returns Processes for all PIDs."""
        collector = Collector(proc=proc_dir)
        assert sorted(process.pid for process in collector.collect()) == pids

    def test_collector_with_pids(self, proc_dir):
        """If PIDs are provided, only those are included."""
        collector = Collector(proc=proc_dir, pids=(10, 30))
        assert sorted(process.pid for process in collector.collect()) == [
            10,
            30,
        ]

    def test_collector_with_pids_sorts(self, proc_dir):
        """Processes are listed in PID order."""
        collector = Collector(proc=proc_dir, pids=(20, 10))
        assert sorted(process.pid for process in collector.collect()) == [
            10,
            20,
        ]

    def test_collector_skip_non_existing(self, proc_dir):
        """Collector skips non-existing processes."""
        collector = Collector(proc=proc_dir, pids=(10, 50))
        assert [process.pid for process in collector.collect()] == [10]


@pytest.fixture
def processes_comm(pids, make_process_dir):
    comms = ["foo", "zza", "bar"]
    for pid, comm in zip(pids, comms):
        (make_process_dir(pid) / "comm").write_text(comm)


@pytest.fixture
def collector(proc_dir, pids):
    collector_pids = pids.copy()
    random.shuffle(collector_pids)  # Not ordered so tests can sort
    yield Collector(proc=proc_dir, pids=collector_pids)


@pytest.fixture
def process_list(proc_dir):
    yield lambda pids: [Process(pid, proc_dir / str(pid)) for pid in pids]


@pytest.mark.usefixtures("processes_comm")
class TestCollection:
    def test_default_collector(self):
        """If a collector is not specified, one that looks at /proc is set."""
        collection = Collection()
        assert collection._collector._proc == Path("/proc")

    def test_iter(self, collector, process_list, pids):
        """Collector is an iterable yielding Processes."""
        collection = Collection(collector=collector)
        assert list(collection) == process_list(pids)

    def test_sort_by(self, collector, process_list):
        """Collector can sort by the specified Process stat."""
        collection = Collection(collector=collector, sort_by="comm")
        assert list(collection) == process_list([30, 10, 20])

    def test_sort_by_reversed(self, collector, process_list):
        """Collector can sort in reverse order."""
        collection = Collection(collector=collector, sort_by="-comm")
        assert list(collection) == process_list([20, 10, 30])

    def test_add_filter(self, collector, process_list):
        """Collector.add_filter adds a filter for processes."""
        collection = Collection(collector=collector)
        collection.add_filter(lambda proc: proc.pid != 20)
        assert list(collection) == process_list([10, 30])

    def test_filter_multiple(self, collector, process_list):
        """Multiple filters can be added."""
        collection = Collection(collector=collector)
        collection.add_filter(lambda proc: proc.pid != 20)
        collection.add_filter(lambda proc: proc.pid != 30)
        assert list(collection) == process_list([10])

    def test_filter_exclusive(self, collector):
        """Filters are applied in 'or'."""
        collection = Collection(collector=collector)
        collection.add_filter(lambda proc: proc.pid == 10)
        collection.add_filter(lambda proc: proc.pid != 10)
        assert list(collection) == []

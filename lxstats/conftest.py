from pathlib import Path

import pytest

from .process import (
    Collection,
    Collector,
    Process,
)


@pytest.fixture
def tmpfile(tmpdir):
    """A temporary file"""
    yield Path(tmpdir / 'file')


@pytest.fixture
def proc_dir(tmpdir):
    """A /proc path."""
    path = Path(tmpdir / 'proc')
    path.mkdir()
    yield path


@pytest.fixture
def make_process_dir(proc_dir):
    """Return a function to create /proc/<pid> dir for a process."""

    def create(pid):
        pid_dir = proc_dir / str(pid)
        pid_dir.mkdir()
        return pid_dir

    yield create


@pytest.fixture
def process_pid():
    """A sample process/task PID."""
    yield 10


@pytest.fixture
def process_dir(process_pid, make_process_dir):
    """The base dir for a sample process."""
    yield make_process_dir(process_pid)


@pytest.fixture
def process(process_pid, process_dir):
    yield Process(process_pid, process_dir)


@pytest.fixture
def processes_pids(make_process_dir):
    """A couple of processes with their cmdline set."""
    proc1_dir = make_process_dir(10)
    (proc1_dir / 'cmdline').write_text('/bin/foo')
    proc2_dir = make_process_dir(20)
    (proc2_dir / 'cmdline').write_text('/bin/bar')
    yield (10, 20)


@pytest.fixture
def collection(proc_dir, processes_pids):
    """A Collection of with sample processes."""
    collector = Collector(proc=proc_dir, pids=processes_pids)
    yield Collection(collector=collector)

from datetime import datetime

import pytest

from ..process import (
    Task,
    TaskBase,
)


@pytest.fixture
def task_base(process_pid, process_dir):
    yield TaskBase(process_pid, process_dir)


class TestTaskBase:
    def test_repr(self, task_base, process_pid):
        """__repr__ includes the task ID."""
        assert repr(task_base) == f"TaskBase({process_pid})"

    def test_id(self, task_base, process_pid):
        """The id attribute returns the task identifier."""
        assert task_base._id == process_pid

    def test_exists(self, task_base, process_dir):
        """It's possible to check whether a process exists."""
        assert task_base.exists
        process_dir.rmdir()
        assert not task_base.exists

    def test_collect_stats(self, task_base, process_dir):
        """Stats are collected from proc when collect_stats is called."""
        assert task_base.available_stats() == []
        (process_dir / "cmdline").write_text("cmd")
        task_base.collect_stats()
        assert task_base.available_stats() == ["cmdline"]

    def test_collect_stats_no_proc_dir(self, task_base, process_dir):
        """If the task dir is not found, stats are left empty."""
        task_base.collect_stats()
        assert task_base.available_stats() == []
        assert task_base.stats() == {}

    def test_collect_stats_prefix(self, task_base, process_dir):
        """The file prefix is used if it reports multiple stats."""
        (process_dir / "statm").write_text("1 2 3 4 5 6 7")
        task_base.collect_stats()
        assert task_base.stats() == {
            "statm.size": 1,
            "statm.resident": 2,
            "statm.share": 3,
            "statm.text": 4,
            "statm.lib": 5,
            "statm.data": 6,
            "statm.dt": 7,
        }

    def test_collect_stats_unreadable_file(self, task_base, process_dir):
        """Unreadable files are skipped when reading stats."""
        cmdline_file = process_dir / "cmdline"
        cmdline_file.write_text("cmd")
        cmdline_file.chmod(0o200)
        task_base.collect_stats()
        assert task_base.available_stats() == []

    def test_collect_stats_not_parsable(self, task_base, process_dir):
        """Stats are not collected for entries that are not parsable files."""
        (process_dir / "task").mkdir()
        task_base.collect_stats()
        assert task_base.available_stats() == []

    def test_collect_stats_ioerror(self, mocker, task_base, process_dir):
        """If reading a file raises an IOError, the stat is skipped."""
        mock_parse = mocker.patch("lxstats.files.text.ParsedFile.parse")
        mock_parse.side_effect = IOError()
        (process_dir / "cmdline").write_text("cmd")
        task_base.collect_stats()
        assert task_base.available_stats() == []

    def test_cmd_from_cmdline(self, task_base, process_dir):
        """TaskBase.cmd parses the content of cmdline if not empty."""
        (process_dir / "cmdline").write_text("cmd\x00with\x00args\x00")
        task_base.collect_stats()
        assert "comm" not in task_base.available_stats()
        assert task_base.get("cmdline") == ["cmd", "with", "args"]
        assert task_base.cmd == "cmd with args"

    def test_cmd_from_comm(self, task_base, process_dir):
        """If cmdline is empty, comm is read."""
        (process_dir / "comm").write_text("cmd")
        task_base.collect_stats()
        assert "cmdline" not in task_base.available_stats()
        assert task_base.cmd == "[cmd]"

    def test_cmd_empty(self, task_base, process_dir):
        """If cmdline and cmd are not found, an empty string is returned."""
        task_base.collect_stats()
        assert task_base.cmd == ""

    def test_timestamp_empty(self, task_base, process_dir):
        """The timestamp is None when stats have not been collected."""
        (process_dir / "cmdline").write_text("cmd")
        assert task_base.timestamp is None

    def test_timestamp(self, task_base, process_dir):
        """The timestamp is None when stats have not been collected."""
        (process_dir / "cmdline").write_text("cmd")
        now = datetime.utcnow()
        task_base._utcnow = lambda: now
        task_base.collect_stats()
        assert task_base.timestamp == now

    def test_available_stats(self, task_base, process_dir):
        """Available Process stats can be listed."""
        (process_dir / "comm").write_text("cmd")
        (process_dir / "wchan").write_text("0")
        task_base.collect_stats()
        assert task_base.available_stats() == ["comm", "wchan"]

    def test_stats(self, task_base, process_dir):
        """Available Process  stats can be returned as a dict ."""
        (process_dir / "comm").write_text("cmd")
        (process_dir / "wchan").write_text("0")
        task_base.collect_stats()
        assert task_base.stats() == {"comm": "cmd", "wchan": "0"}

    def test_get(self, task_base, process_dir):
        """Value for a stat can be returned."""
        (process_dir / "wchan").write_text("poll_schedule_timeout")
        task_base.collect_stats()
        assert task_base.get("wchan") == "poll_schedule_timeout"

    def test_get_not_found(self, task_base, process_dir):
        """If the requested stat is not found, None is returned."""
        task_base.collect_stats()
        assert task_base.get("wchan") is None

    def test_get_cmd(self, task_base, process_dir):
        """The get() method can return the cmd."""
        (process_dir / "cmdline").write_text("cmd")
        task_base.collect_stats()
        assert task_base.get("cmd") == "cmd"

    def test_equal(self, task_base, process_dir, process_pid):
        """Two TaskBases are equal if they have the same pid."""
        other = TaskBase(process_pid, process_dir)
        different = TaskBase(process_pid + 1, process_dir)
        assert task_base == other
        assert task_base != different

    def test_hash(self, task_base, process_dir, process_pid):
        """Two TaskBases have the same hash if they have hte same id."""
        other = TaskBase(process_pid, process_dir / "other")
        assert hash(task_base) == hash(other)


class TestProcess:
    def test_pid(self, process, process_pid):
        """The pid attribute returns the PID."""
        assert process.pid == process_pid

    def test_get_pid(self, process, process_pid):
        """The get() method can return the PID."""
        process.collect_stats()
        assert process.get("pid") == process_pid

    def test_tasks(self, process, process_dir):
        """The list of TIDs for process tasks can be returned."""
        (process_dir / "task").mkdir()
        (process_dir / "task/123").touch()
        (process_dir / "task/456").touch()
        assert process.tasks() == [
            Task(123, process, process_dir / "task/123"),
            Task(456, process, process_dir / "task/456"),
        ]


@pytest.fixture
def task(process, process_pid):
    yield Task(process_pid, process, process._dir._path / f"task/{process_pid}")


class TestTask:
    def test_pid(self, task, process_pid):
        """The tid attribute returns the TID."""
        assert task.tid == process_pid

    def test_process(self, task, process):
        """The parent attribute returns the task parent process."""
        assert task.parent == process

    def test_get_pid(self, task, process_pid):
        """The get() method can return the PID."""
        task.collect_stats()
        assert task.get("tid") == process_pid

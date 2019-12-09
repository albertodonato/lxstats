import pytest

from ..filter import (
    CommandLineFilter,
    CommandNameFilter,
)


class TestCommandNameFilter:
    @pytest.mark.parametrize(
        "cmdline,matches", [("foo\x00bar\x00", True), ("/bin/foo\x00", False)]
    )
    def test_filter_match(self, process, process_dir, cmdline, matches):
        """CommandNameFilter matches a process by exact cmdline."""
        proc_filter = CommandNameFilter("foo")
        (process_dir / "cmdline").write_text(cmdline)
        process.collect_stats()
        assert proc_filter(process) == matches

    def test_filter_matching_comm(self, process, process_dir):
        """CommandNameFilter matches a process by comm value."""
        proc_filter = CommandNameFilter("foo")
        (process_dir / "comm").write_text("foo")
        process.collect_stats()
        assert proc_filter(process)


class TestCommandLineFilter:
    @pytest.mark.parametrize(
        "cmdline,matches",
        [("/bin/foo\x00bar\x00", True), ("/bin/bar\x00foo\x00", False)],
    )
    def test_filter_matching_process(self, process, process_dir, cmdline, matches):
        """CommandLineFilter matches a process by command line."""
        proc_filter = CommandLineFilter("foo")
        (process_dir / "cmdline").write_text(cmdline)
        process.collect_stats()
        assert proc_filter(process) == matches

    def test_include_args(self, process, process_dir):
        """Arguments are included in match if include_args is True."""
        proc_filter = CommandLineFilter("foo", include_args=True)
        (process_dir / "cmdline").write_text("/bin/bar\x00foo\x00")
        process.collect_stats()
        assert proc_filter(process)

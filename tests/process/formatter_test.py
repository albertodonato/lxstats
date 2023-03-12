from io import StringIO

import pytest

from lxstats.process import Process
from lxstats.process.collection import (
    Collection,
    Collector,
)
from lxstats.process.formatter import Formatter


class SampleFormatter(Formatter):
    config = {"option": 10}
    endl = "\n"

    def _format_header(self):
        self._write("header\n")

    def _format_footer(self):
        self._write("footer\n")

    def _format_process(self, process):
        self._write(f"process {process.pid} {process.cmd}\n")

    def _dump(self):
        self._write("dump\n")


@pytest.mark.usefixtures("processes_pids")
class TestFormatter:
    def test_format_no_op_default(self, proc_dir):
        """By default, format methods don't output anything."""
        stream = StringIO()
        (proc_dir / "10/cmdline").write_text("cmd1")
        (proc_dir / "20/cmdline").write_text("cmd2")
        collector = Collector(proc=proc_dir, pids=(10, 20))
        collection = Collection(collector=collector)
        formatter = Formatter(stream, ["pid"])
        formatter.format(collection)
        assert stream.getvalue() == ""

    def test_format(self, proc_dir):
        """Formatter.format outputs process info with header and footer."""
        stream = StringIO()
        (proc_dir / "10/cmdline").write_text("cmd1")
        (proc_dir / "20/cmdline").write_text("cmd2")
        collector = Collector(proc=proc_dir, pids=(10, 20))
        collection = Collection(collector=collector)
        formatter = SampleFormatter(stream, ["pid", "cmd"])
        formatter.format(collection)
        assert stream.getvalue() == (
            "header\n"
            "process 10 cmd1\n"
            "process 20 cmd2\n"
            "footer\n"
            "dump\n"
        )

    def test_fields_values(self, proc_dir):
        """Formatter._fields_values returns a list with Process values."""
        (proc_dir / "10/cmdline").write_text("/bin/foo")
        formatter = SampleFormatter(StringIO(), ["pid", "cmd"])
        process = Process(10, proc_dir / "10")
        process.collect_stats()
        assert formatter._fields_values(process) == [10, "/bin/foo"]

    def test_config_default_value(self):
        """Formatter can have config options with default values."""
        formatter = SampleFormatter(StringIO(), ["pid", "cmdline"])
        assert formatter._config == {"option": 10}

    def test_config_set_value(self):
        """It's possible to specify config options to Formatter."""
        formatter = SampleFormatter(StringIO(), ["pid", "cmdline"], option=30)
        assert formatter._config == {"option": 30}

    def test_unknown_option(self):
        """If an unknown option is specified, an error is raised."""
        with pytest.raises(TypeError):
            SampleFormatter(StringIO(), ["pid", "cmdline"], unknown_option=30)

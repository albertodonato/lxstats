from textwrap import dedent

from ..process import (
    ProcPIDCgroup,
    ProcPIDCmdline,
    ProcPIDEnviron,
    ProcPIDIo,
    ProcPIDNs,
    ProcPIDSched,
    ProcPIDStat,
    ProcPIDStatm,
    ProcPIDStatus,
)


class TestProcPIDCmdline:
    def test_parse(self, tmpfile):
        """Command line tokens are parsed and split into a list."""
        tmpfile.write_text("/bin/foo\x00bar\x00baz\x00")
        cmdline_file = ProcPIDCmdline(tmpfile)
        assert cmdline_file.parse() == ["/bin/foo", "bar", "baz"]

    def test_parse_with_spaces(self, tmpfile):
        """Command or arguments can contain spaces."""
        tmpfile.write_text("/bin/foo bar\x00baz bza\x00")
        cmdline_file = ProcPIDCmdline(tmpfile)
        assert cmdline_file.parse() == ["/bin/foo bar", "baz bza"]


class TestProcPIDStat:
    def test_fields(self, tmpfile):
        """Fields and values from /proc/[pid]/stat files are reported."""
        tmpfile.write_text(" ".join(str(i) for i in range(45)))
        stat_file = ProcPIDStat(tmpfile)
        assert stat_file.parse() == {
            "pid": 0,
            "comm": "1",
            "state": "2",
            "ppid": 3,
            "pgrp": 4,
            "session": 5,
            "tty_nr": 6,
            "tpgid": 7,
            "flags": 8,
            "minflt": 9,
            "cminflt": 10,
            "majflt": 11,
            "cmajflt": 12,
            "utime": 13,
            "stime": 14,
            "cutime": 15,
            "cstime": 16,
            "priority": 17,
            "nice": 18,
            "num_threads": 19,
            "itrealvalue": 20,
            "starttime": 21,
            "vsize": 22,
            "rss": 23,
            "rsslim": 24,
            "startcode": 25,
            "endcode": 26,
            "startstack": 27,
            "kstkesp": 28,
            "kstkeip": 29,
            "exit_signal": 37,
            "processor": 38,
            "rt_priority": 39,
            "policy": 40,
            "delayacct_blkio_ticks": 41,
            "guest_time": 42,
            "cguest_time": 43,
        }

    def test_comm_with_spaces(self, tmpfile):
        """The comm field can contain spaces.."""
        fields = [str(i) for i in range(45)]
        # Set a comm field with spaces
        fields[1] = "(cmd with spaces)"
        tmpfile.write_text(" ".join(fields))
        stat_file = ProcPIDStat(tmpfile)
        assert stat_file.parse()["comm"] == "cmd with spaces"


class TestProcPIDStatm:
    def test_fields(self, tmpfile):
        """Fields and values from /proc/[pid]/statm files are reported."""
        tmpfile.write_text("1 2 3 4 5 6 7")
        statm_file = ProcPIDStatm(tmpfile)
        assert statm_file.parse() == {
            "size": 1,
            "resident": 2,
            "share": 3,
            "text": 4,
            "lib": 5,
            "data": 6,
            "dt": 7,
        }


class TestProcPIDIo:
    def test_fields(self, tmpfile):
        """Fields and values from /proc/[pid]/io files are reported."""
        tmpfile.write_text(
            dedent(
                """\
                rchar: 100
                wchar: 200
                syscr: 300
                syscw: 400
                read_bytes: 500
                write_bytes: 600
                cancelled_write_bytes: 700
                """
            )
        )
        io_file = ProcPIDIo(tmpfile)
        assert io_file.parse() == {
            "rchar": 100,
            "wchar": 200,
            "syscr": 300,
            "syscw": 400,
            "read_bytes": 500,
            "write_bytes": 600,
            "cancelled_write_bytes": 700,
        }


class TestProcPIDNs:
    def test_parse(self, tmpdir):
        """The pid of each namespace from the link name is returned."""
        (tmpdir / "pid").mksymlinkto("pid:[123]")
        (tmpdir / "ipc").mksymlinkto("ipc:[456]")
        ns_dir = ProcPIDNs(tmpdir)
        assert ns_dir.parse() == {"pid": 123, "ipc": 456}


class TestProcPIDSched:
    def test_fields(self, tmpfile):
        """Fields and values from /proc/[pid]/sched files are parsed."""
        content = dedent(
            """\
            process (1234, #threads: 1)
            -------------------------------------------------------------------
            se.exec_start                                :     123456789.123456
            se.vruntime                                  :       1234567.123456
            se.sum_exec_runtime                          :             0.123456
            se.statistics.sum_sleep_runtime              :             1.234567
            current_node=0, numa_group_id=0
            numa_faults node=0 task_private=0 task_shared=0 group_private=0
            """
        )
        tmpfile.write_text(content)
        io_file = ProcPIDSched(tmpfile)
        assert io_file.parse() == {
            "se.exec_start": 123456789.123456,
            "se.vruntime": 1234567.123456,
            "se.sum_exec_runtime": 0.123456,
            "se.statistics.sum_sleep_runtime": 1.234567,
        }


class TestProcPIDEnviron:
    def test_parse(self, tmpfile):
        """Environment variables are returned as a dict."""
        tmpfile.write_text("FOO=foo\x00BAR=bar\x00")
        environ_file = ProcPIDEnviron(tmpfile)
        assert environ_file.parse() == {"FOO": "foo", "BAR": "bar"}

    def test_parse_single_value(self, tmpfile):
        """If the = sign is not present, the line is used as key."""
        tmpfile.write_text("someline\x00BAR=bar\x00")
        environ_file = ProcPIDEnviron(tmpfile)
        assert environ_file.parse() == {"someline": None, "BAR": "bar"}


class TestProcPIDCgroup:
    def test_parse(self, tmpfile):
        """A dict is returned with hierarchy id as key."""
        content = dedent(
            """\
            6:hugetlb:/group2
            5:net_cls,net_prio:/group1
            4:blkio:/group2
            3:cpu,cpuacct:/group1
            2:devices:/group1
            """
        )
        tmpfile.write_text(content)
        cgroup_file = ProcPIDCgroup(tmpfile)
        assert cgroup_file.parse() == {
            6: (["hugetlb"], "/group2"),
            5: (["net_cls", "net_prio"], "/group1"),
            4: (["blkio"], "/group2"),
            3: (["cpu", "cpuacct"], "/group1"),
            2: (["devices"], "/group1"),
        }


class TestProcPIDStatus:
    def test_parse(self, tmpfile):
        """A dict with memory information for the file is returned."""
        content = dedent(
            """\
            VmPeak:\t 1132616 kB
            VmSize:\t 1115196 kB
            VmLck:\t       0 kB
            VmPin:\t       0 kB
            VmHWM:\t  246340 kB
            VmRSS:\t  246340 kB
            RssAnon:\t  210612 kB
            RssFile:\t   35700 kB
            RssShmem:\t      28 kB
            VmData:\t  292668 kB
            VmStk:\t     548 kB
            VmExe:\t    2436 kB
            VmLib:\t  136932 kB
            VmPTE:\t    1272 kB
            VmPMD:\t      16 kB
            VmSwap:\t       0 kB
            HugetlbPages:\t       0 kB
            """
        )
        tmpfile.write_text(content)
        status_file = ProcPIDStatus(tmpfile)
        assert status_file.parse() == {
            "VmPeak": 1159798784,
            "VmSize": 1141960704,
            "VmLck": 0,
            "VmPin": 0,
            "VmHWM": 252252160,
            "VmRSS": 252252160,
            "RssAnon": 215666688,
            "RssFile": 36556800,
            "RssShmem": 28672,
            "VmData": 299692032,
            "VmStk": 561152,
            "VmExe": 2494464,
            "VmLib": 140218368,
            "VmPTE": 1302528,
            "VmPMD": 16384,
            "VmSwap": 0,
            "HugetlbPages": 0,
        }

    def test_parse_skip_extra(self, tmpfile):
        """Non memory-related info is skipped."""
        content = dedent(
            """\
            Uid:\t1000	1000	1000	1000
            Gid:\t1000	1000	1000	1000
            VmPeak:\t 1132616 kB
            VmSize:\t 1115196 kB
            """
        )
        tmpfile.write_text(content)
        status_file = ProcPIDStatus(tmpfile)
        assert status_file.parse() == {"VmPeak": 1159798784, "VmSize": 1141960704}

    def test_parse_split_in_two(self, tmpfile):
        """Lines containing more than one ':' are split in two."""
        content = dedent(
            """\
            VmPeak:\t 1132616 kB
            Line: with more: semicolons
            VmSize:\t 1115196 kB
            """
        )
        tmpfile.write_text(content)
        status_file = ProcPIDStatus(tmpfile)
        assert status_file.parse() == {"VmPeak": 1159798784, "VmSize": 1141960704}

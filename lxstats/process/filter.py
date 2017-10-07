"""Filter classes for process Collection."""

import re


class CommandNameFilter:
    """Filter processes based on the command name.

    Parameters:
      name: the name of the command.

    """

    def __init__(self, name):
        self._name = name

    def __call__(self, process):
        cmdline = process.get('cmdline')
        if cmdline:
            return cmdline[0] == self._name

        return process.get('comm') == self._name


class CommandLineFilter:
    """Filter Processes based on the command line.

    Parameters:
      regexp: a regexp to match the commandline.
      include_args: whether include args in match.

    """

    def __init__(self, regexp, include_args=False):
        self._re = re.compile(regexp)
        self._include_args = include_args

    def __call__(self, process):
        cmd = process.cmd
        if not self._include_args:
            cmd = cmd.split()[0]
        return bool(self._re.findall(cmd))

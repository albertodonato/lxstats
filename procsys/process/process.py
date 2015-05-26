#
# This file is part of ProcSys.
#
# ProcSys is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# ProcSys is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ProcSys.  If not, see <http://www.gnu.org/licenses/>.

'''Hold information about a running process.'''

from procsys.files.proc import ProcPIDDirectory


class Process:
    '''Retrieve and hold information about a given process.'''

    def __init__(self, pid, proc_dir):
        self.pid = pid
        self._dir = ProcPIDDirectory(proc_dir)
        self._stats = {}

    @property
    def cmd(self):
        '''The process command line, with brackets for kernel processes.'''
        cmdline = self._stats.get('cmdline')
        if cmdline:
            return ' '.join(cmdline)
        comm = self._stats.get('comm')
        return '[{}]'.format(comm) if comm else ''

    def exists(self):
        '''Whether the process exists.'''
        return self._dir.exists()

    def collect_stats(self):
        '''Collect stats about the process from /proc files.'''
        self._stats = {}  # Reset

        if not self._dir.readable():
            return

        for name in self._dir.list():
            if not self._dir[name].readable():
                continue

            parsed_stats = self._dir[name].read()
            if isinstance(parsed_stats, dict):
                self._stats.update(
                    ('{}.{}'.format(name, key), value)
                    for key, value in parsed_stats.items())
            else:
                self._stats[name] = parsed_stats

    def available_stats(self):
        '''Return a sorted list of available stats for the process.'''
        return sorted(self._stats)

    def stats(self):
        '''Return a dict with process stats.'''
        return self._stats.copy()

    def get(self, stat):
        '''Return the stat with the name name, or None if not available.'''
        if stat in ('pid', 'cmd'):
            return getattr(self, stat)

        return self._stats.get(stat)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.pid)

    def __eq__(self, other):
        return self.pid == other.pid

    def __hash__(self):
        return hash((self.__class__, self.pid))

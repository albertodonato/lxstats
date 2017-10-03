"""Hold information about a running process.

Stats for a process can be collected and accessed::

p = Process(123, '/proc/123')
p.collect_stats()
p.get('statm.size')

"""

from datetime import datetime

from ..files.proc import ProcProcessDirectory


class TaskBase:
    """Base class for tasks and processes."""

    _utcnow = datetime.utcnow  # For testing

    _id_attr = '_id'

    def __init__(self, id, proc_dir):
        self._id = id
        self._dir = ProcProcessDirectory(proc_dir)
        self._reset()

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._id)

    def __eq__(self, other):
        return self._id == other._id

    def __hash__(self):
        return hash((self.__class__, self._id))

    @property
    def cmd(self):
        """The task command line, with brackets for kernel tasks."""
        cmdline = self._stats.get('cmdline')
        if cmdline:
            return ' '.join(cmdline)
        comm = self._stats.get('comm')
        return '[{}]'.format(comm) if comm else ''

    @property
    def exists(self):
        """Whether the task exists."""
        return self._dir.exists

    def collect_stats(self):
        """Collect stats about the process from ``/proc`` files."""
        self._reset()

        if not self._dir.readable:
            return

        self._timestamp = self._utcnow()

        for name in self._dir.list():
            entry = self._dir[name]
            if not entry.readable or not hasattr(entry, 'parse'):
                continue

            try:
                parsed_stats = entry.parse()
            except IOError:
                continue

            if isinstance(parsed_stats, dict):
                self._stats.update(
                    ('{}.{}'.format(name, key), value)
                    for key, value in parsed_stats.items())
            else:
                self._stats[name] = parsed_stats

    def available_stats(self):
        """Return a sorted list of available stats for the process."""
        return sorted(self._stats)

    def stats(self):
        """Return a dict with process stats."""
        return self._stats.copy()

    @property
    def timestamp(self):
        """Return the timestamp for stat collection."""
        return self._timestamp

    def get(self, stat):
        """Return the stat with the name, or None if not available."""
        if stat in (self._id_attr, 'cmd', 'timestamp'):
            return getattr(self, stat)

        return self._stats.get(stat)

    def _reset(self):
        """Reset stats."""
        self._stats = {}
        self._timestamp = None


class Process(TaskBase):
    """Retrieve and hold information about a given process."""

    _utcnow = datetime.utcnow  # For testing

    _id_attr = 'pid'

    @property
    def pid(self):
        """The process PID."""
        return self._id

    def tasks(self):
        """Return a list of Tasks for the Process."""
        tasks = []
        tasks_dir = self._dir['task']
        for tid in tasks_dir.listdir():
            tasks.append(Task(int(tid), self, tasks_dir.join(tid)))
        return tasks


class Task(TaskBase):
    """Retrieve and hold information about a given task."""

    _id_attr = 'tid'

    def __init__(self, id, parent, proc_dir):
        super().__init__(id, proc_dir)
        self.parent = parent

    @property
    def tid(self):
        """The task TID."""
        return self._id

"""
Handle collection of processes, allowing filtering and sorting by attribute
values.
"""

from os import path
from glob import iglob

from .process import Process


class Collector:
    """Process collector.

    An iterable with PIDs can be passed, otherwise all PIDs found scanning
    the ``/proc`` directory are returned.

    """
    def __init__(self, proc='/proc', pids=()):
        self._proc = '{}/'.format(path.normpath(proc))
        self._pids = pids

    def collect(self):
        """Return an iterator yielding Process objects."""
        if self._pids:
            proc_dirs = (
                '{}{}'.format(self._proc, pid) for pid in sorted(self._pids))
        else:
            proc_dirs = iglob('{}[0-9]*'.format(self._proc))

        l = len(self._proc)
        for proc_dir in proc_dirs:
            process = Process(int(proc_dir[l:]), proc_dir)
            process.collect_stats()
            if process.exists:
                # Don't return non-existing processes. Check this after trying
                # collecting stats, since doing the opposite there's a chance
                # the process might go away bewteen the check and the
                # data collection.
                yield process


class Collection:
    """A Process collection.

    Parameters:
      collector: A ProcessCollector instance. If not provided, a default one
        will be created.
      sort_by: The field to sort processes by. It can be prefixed with ``-``
        to invert sorting (e.g. ``pid`` or ``-pid``).

    """

    def __init__(self, collector=None, sort_by=None):
        if collector is None:
            self._collector = Collector()
        else:
            self._collector = collector
        self._filters = []
        self._set_sort_by(sort_by)

    def add_filter(self, filter_function):
        """Add a filtering function to the collection.

        Processes not matching the filter are not returned.

        Parameters:
          filter_function: A callable accepting a Process and returning a
            boolean value (whether the process should be included).

        """
        self._filters.append(filter_function)

    def __iter__(self):
        """Return an iterator yielding Process objects.

        Processes are filtered and sorted as configured.

        """
        iterator = self._collector.collect()
        if self._filters:
            iterator = filter(self._filter, iterator)

        if self._sort_by is not None:
            def key(elem):
                return elem.get(self._sort_by)

            iterator = iter(sorted(
                iterator, key=key, reverse=self._sort_reverse))

        return iterator

    def _filter(self, proc):
        """Apply filters to a Process."""
        return all(ffunc(proc) for ffunc in self._filters)

    def _set_sort_by(self, sort_by):
        if sort_by is not None and sort_by.startswith('-'):
            self._sort_by = sort_by[1:]
            self._sort_reverse = True
        else:
            self._sort_by = sort_by
            self._sort_reverse = False

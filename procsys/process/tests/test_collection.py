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

from os import path

from procsys.testing import TestCase

from procsys.process.process import Process
from procsys.process.collection import Collector, Collection


class CollectorTests(TestCase):

    def test_collector_scan(self):
        '''The Collector returns Processes for all PIDs.'''
        self.make_process_file(10, 'cmdline')
        self.make_process_file(20, 'cmdline')
        self.make_process_file(30, 'cmdline')
        collector = Collector(proc=self.tempdir.path)
        self.assertCountEqual(
            (process.pid for process in collector.collect()),
            [10, 20, 30])

    def test_collector_with_pids(self):
        '''If PIDs are provided, only those are included.'''
        self.make_process_file(10, 'cmdline')
        self.make_process_file(20, 'cmdline')
        self.make_process_file(30, 'cmdline')
        collector = Collector(proc=self.tempdir.path, pids=(10, 30))
        self.assertCountEqual(
            (process.pid for process in collector.collect()),
            [10, 30])

    def test_collector_with_pids_sorts(self):
        '''Processes are listed in PID order.'''
        self.make_process_file(10, 'cmdline')
        self.make_process_file(20, 'cmdline')
        collector = Collector(proc=self.tempdir.path, pids=(20, 10))
        self.assertCountEqual(
            (process.pid for process in collector.collect()),
            [10, 20])

    def test_collector_skip_non_existing(self):
        '''Collector skips non-existing processes.'''
        self.make_process_file(10, 'cmdline')
        collector = Collector(proc=self.tempdir.path, pids=(10, 20))
        self.assertEqual(
            [process.pid for process in collector.collect()], [10])


class CollectionTests(TestCase):

    def setUp(self):
        super().setUp()
        pids = (10, 30, 20)  # Not ordered so tests can sort
        self.collector = Collector(proc=self.tempdir.path, pids=pids)
        self.make_process_file(10, 'comm', content='foo')
        self.make_process_file(20, 'comm', content='zza')
        self.make_process_file(30, 'comm', content='bar')

    def process_list(self, pids):
        '''Return a list of processes with specified pids.'''
        return [
            Process(pid, path.join(self.tempdir.path, str(pid)))
            for pid in pids]

    def test_iter(self):
        '''Collector is an iterable yielding Processes.'''
        collection = Collection(collector=self.collector)
        self.assertCountEqual(collection, self.process_list([10, 20, 30]))

    def test_sort_by(self):
        '''Collector can sort by the specified Process stat.'''
        collection = Collection(collector=self.collector, sort_by='comm')
        self.assertEqual(list(collection), self.process_list([30, 10, 20]))

    def test_sort_by_reversed(self):
        '''Collector can sort in reverse order.'''
        collection = Collection(collector=self.collector, sort_by='-comm')
        self.assertEqual(list(collection), self.process_list([20, 10, 30]))

    def test_add_filter(self):
        '''Collector.add_filter adds a filter for processes.'''
        collection = Collection(collector=self.collector)
        collection.add_filter(lambda proc: proc.pid != 20)
        self.assertCountEqual(collection, self.process_list([10, 30]))

    def test_filter_multiple(self):
        '''Multiple filters can be added.'''
        collection = Collection(collector=self.collector)
        collection.add_filter(lambda proc: proc.pid != 20)
        collection.add_filter(lambda proc: proc.pid != 30)
        self.assertCountEqual(collection, self.process_list([10]))

    def test_filter_exclusive(self):
        '''Filters are applied in 'or'.'''
        collection = Collection(collector=self.collector)
        collection.add_filter(lambda proc: proc.pid == 10)
        collection.add_filter(lambda proc: proc.pid != 10)
        self.assertCountEqual(collection, [])

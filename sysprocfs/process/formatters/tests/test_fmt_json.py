#
# This file is part of SysProcFS.
#
# SysProcFS is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# SysProcFS is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# SysProcFS.  If not, see <http://www.gnu.org/licenses/>.

import json
from io import StringIO

from ....testing import TestCase
from .. import JSONFormatter
from ...collection import Collector, Collection


class JSONFormatterTests(TestCase):

    def setUp(self):
        super().setUp()
        self.stream = StringIO()
        collector = Collector(proc=self.tempdir.path, pids=(10, 20))
        self.collection = Collection(collector=collector)
        self.make_process_file(10, 'cmdline', content='/bin/foo')
        self.make_process_file(20, 'cmdline', content='/bin/bar')

    def test_format(self):
        '''JSONFormatter formats process info in JSON format.'''
        formatter = JSONFormatter(self.stream, ['pid', 'cmd'])
        formatter.format(self.collection)
        self.assertEqual(
            self.stream.getvalue(),
            json.dumps(
                {'fields': ['pid', 'cmd'],
                 'processes': [
                     {'pid': 10, 'cmd': '/bin/foo'},
                     {'pid': 20, 'cmd': '/bin/bar'}]}))

    def test_format_indent(self):
        '''The indent parameter is passed to the JSON encoder.'''
        formatter = JSONFormatter(self.stream, ['pid', 'cmd'], indent=3)
        formatter.format(self.collection)
        self.assertEqual(
            self.stream.getvalue(),
            json.dumps(
                {'fields': ['pid', 'cmd'],
                 'processes': [
                     {'pid': 10, 'cmd': '/bin/foo'},
                     {'pid': 20, 'cmd': '/bin/bar'}]},
                indent=3))

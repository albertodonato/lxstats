#
# This file is part of ProcSys.

# ProcSys is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# ProcSys is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ProcSys.  If not, see <http://www.gnu.org/licenses/>.

from cStringIO import StringIO

from procsys.testing import TestCase

from procsys.process.formatter import Formatter
from procsys.process.collection import Collection, Collector
from procsys.process.process import Process


class SampleFormatter(Formatter):

    config = {'option': 10}
    endl = '\n'

    def _format_header(self):
        self._write('header\n')

    def _format_footer(self):
        self._write('footer\n')

    def _format_process(self, process):
        self._write('process {} {}\n'.format(process.pid, process.cmd))

    def _dump(self):
        self._write('dump\n')


class FormatterTests(TestCase):

    def setUp(self):
        super(FormatterTests, self).setUp()
        self.stream = StringIO()

    def test_format(self):
        '''Formatter.format outputs process info with header and footer.'''
        self.make_process_file(10, 'cmdline', content='cmd1')
        self.make_process_file(20, 'cmdline', content='cmd2')
        collector = Collector(proc=self.tempdir, pids=(10, 20))
        collection = Collection(collector=collector)
        formatter = SampleFormatter(self.stream, ['pid', 'cmd'])
        formatter.format(collection)
        self.assertEqual(
            self.stream.getvalue(),
            'header\n'
            'process 10 cmd1\n'
            'process 20 cmd2\n'
            'footer\n'
            'dump\n')

    def test_wb_fields_values(self):
        '''Formatter._fields_values returns a list with Process values.'''
        self.make_process_file(10, 'cmdline', '/bin/foo')
        formatter = SampleFormatter(self.stream, ['pid', 'cmd'])
        process = Process(10, proc_dir='{}/10'.format(self.tempdir))
        process.collect_stats()
        self.assertEqual(
            formatter._fields_values(process), [10, '/bin/foo'])

    def test_wb_config_default_value(self):
        '''Formatter can have config options with default values.'''
        formatter = SampleFormatter(self.stream, ['pid', 'cmdline'])
        self.assertEqual(formatter._config, {'option': 10})

    def test_wb_config_set_value(self):
        '''It's possible to specify config options to Formatter.'''
        formatter = SampleFormatter(self.stream, ['pid', 'cmdline'], option=30)
        self.assertEqual(formatter._config, {'option': 30})

    def test_wb_unknown_option(self):
        '''If an unknown option is specified, an error is raised.'''
        self.assertRaises(
            TypeError, SampleFormatter, self.stream, ['pid', 'cmdline'],
            unknown_option=30)

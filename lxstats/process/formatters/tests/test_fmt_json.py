import json
from io import StringIO

from ....testing import TestCase
from .. import JSONFormatter
from ...collection import (
    Collector,
    Collection)


class JSONFormatterTests(TestCase):

    def setUp(self):
        super().setUp()
        self.stream = StringIO()
        collector = Collector(proc=self.tempdir.path, pids=(10, 20))
        self.collection = Collection(collector=collector)
        self.make_process_file(10, 'cmdline', content='/bin/foo')
        self.make_process_file(20, 'cmdline', content='/bin/bar')

    def test_format(self):
        """JSONFormatter formats process info in JSON format."""
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
        """The indent parameter is passed to the JSON encoder."""
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

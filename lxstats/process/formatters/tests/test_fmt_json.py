from io import StringIO
import json

from .. import JSONFormatter


class TestJSONFormatter:
    def test_format(self, collection):
        """JSONFormatter formats process info in JSON format."""
        stream = StringIO()
        formatter = JSONFormatter(stream, ["pid", "cmd"])
        formatter.format(collection)
        assert stream.getvalue() == json.dumps(
            {
                "fields": ["pid", "cmd"],
                "processes": [
                    {"pid": 10, "cmd": "/bin/foo"},
                    {"pid": 20, "cmd": "/bin/bar"},
                ],
            }
        )

    def test_format_indent(self, collection):
        """The indent parameter is passed to the JSON encoder."""
        stream = StringIO()
        formatter = JSONFormatter(stream, ["pid", "cmd"], indent=3)
        formatter.format(collection)
        assert stream.getvalue() == json.dumps(
            {
                "fields": ["pid", "cmd"],
                "processes": [
                    {"pid": 10, "cmd": "/bin/foo"},
                    {"pid": 20, "cmd": "/bin/bar"},
                ],
            },
            indent=3,
        )

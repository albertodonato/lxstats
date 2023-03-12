from pathlib import Path

import pytest
from toolrack.collect import Collection

from ...tracing.tracer import (
    Tracer,
    Tracing,
    UnsupportedTracer,
)
from ...tracing.types import TracerType


@pytest.fixture
def instances_dir(tmpdir):
    instances = tmpdir / "instances"
    instances.mkdir()
    yield instances


@pytest.fixture
def tracing(tmpdir):
    yield Tracing(path=Path(tmpdir))


class TestTracing:
    def test_tracers_empty(self, tracing, instances_dir):
        """If no tracer is defined, an empty list is returned."""
        assert tracing.tracers == []

    def test_tracers_exists(self, tracing, instances_dir):
        """A Tracer object is returned for each tracing directory."""
        (instances_dir / "tracer-1").mkdir()
        (instances_dir / "tracer-2").mkdir()
        for tracer in tracing.tracers:
            assert isinstance(tracer, Tracer)
        assert [tracer.name for tracer in tracing.tracers] == [
            "tracer-1",
            "tracer-2",
        ]

    def test_get_tracer_existing(self, tracing, instances_dir):
        """A Tracer for a specified tracing instance is returned."""
        (instances_dir / "tracer").mkdir()
        tracer = tracing.get_tracer("tracer")
        assert tracer.name == "tracer"

    def test_get_tracer_create(self, tracing, instances_dir):
        """If the requested tracing instance doesn't exist, it's created."""
        tracing.get_tracer("tracer")
        assert (instances_dir / "tracer").exists()

    def test_remove_tracer(self, tracing, instances_dir):
        """A Tracer can be removed."""
        (instances_dir / "tracer").mkdir()
        tracing.remove_tracer("tracer")
        assert not (instances_dir / "tracer").exists()


@pytest.fixture
def tracer(tmpdir):
    yield Tracer(path=Path(tmpdir))


class TestTracer:
    def test_name(self, tmpdir, tracer):
        """The Tracer name is the name of the tracer directory."""
        assert tracer.name == tmpdir.basename

    def test_type(self, tmpdir, tracer):
        """The Tracer type can be returned."""
        (tmpdir / "current_tracer").write_text("nop", "utf-8")
        assert tracer.type == "nop"

    def test_set_type(self, tmpdir, tracer):
        """The Tracer type can be set."""
        (tmpdir / "current_tracer").write_text("func", "utf-8")
        tracer.set_type("nop")
        assert tracer.type == "nop"

    def test_set_type_unsupported(self, tracer):
        """If the Tracer type is unsupported, an error is raised."""
        with pytest.raises(UnsupportedTracer):
            tracer.set_type("unknown")

    @pytest.mark.parametrize("content,enabled", [("1", True), ("0", False)])
    def test_enabled(self, tmpdir, tracer, content, enabled):
        """The Tracer is enabled if the corresponding flag is set."""
        (tmpdir / "tracing_on").write_text(content, "utf-8")
        assert tracer.enabled == enabled

    def test_toggle(self, tmpdir, tracer):
        """The Tracer can be enabled and disabled."""
        (tmpdir / "tracing_on").write_text("1", "utf-8")
        tracer.toggle(True)
        assert tracer.enabled
        tracer.toggle(False)
        assert not tracer.enabled

    def test_options(self, tmpdir, tracer):
        """Tracer options are returned, with their status."""
        (tmpdir / "trace_options").write_text("noraw\nhex", "utf-8")
        assert tracer.options == {"raw": False, "hex": True}

    def test_set_option(self, tmpdir, tracer):
        """Tracer options can be set."""
        (tmpdir / "trace_options").write_text("nohex", "utf-8")
        assert tracer.options == {"hex": False}
        tracer.set_option("hex", True)
        assert tracer.options == {"hex": True}
        tracer.set_option("hex", False)
        assert tracer.options == {"hex": False}

    def test_trace_content(self, tmpdir, tracer):
        """The trace file content can be returned."""
        (tmpdir / "trace").write_text("some trace content", "utf-8")
        assert tracer.trace() == "some trace content"

    def test_trace_pipe(self, tmpdir, tracer):
        """The trace_pipe file cam be returned and read."""
        (tmpdir / "trace_pipe").write_text("some trace content", "utf-8")
        with tracer.trace_pipe() as pipe:
            assert pipe.read() == "some trace content"

    def test_attribute_access(self, tmpdir, tracer):
        """Attribute specific to the tracer type can be accessed."""

        class SampleTracer(TracerType):
            name = "sample"

            foo = "a sample attribute"

        tracer._tracer_types = Collection("TracerType", "name")
        tracer._tracer_types.add(SampleTracer)

        (tmpdir / "current_tracer").write_text("", "utf-8")
        tracer.set_type("sample")
        assert tracer.foo == "a sample attribute"

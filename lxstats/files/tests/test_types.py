import pytest

from ..types import (
    OptionsFile,
    SelectableOptionsFile,
    TogglableOptionsFile,
    ToggleFile,
    ValueFile,
)


@pytest.fixture
def options_file(tmpfile):
    yield OptionsFile(tmpfile)


class TestOptionsFile:

    @pytest.mark.parametrize(
        'content',
        [
            'foo bar baz',  # space-separated
            'foo\nbar\nbaz',  # newline-separated
            'foo [bar] baz'  # with selected option
        ])
    def test_options(self, options_file, tmpfile, content):
        """Option values can be listed."""
        tmpfile.write_text(content)
        assert options_file.options == ['foo', 'bar', 'baz']


@pytest.fixture
def select_file(tmpfile):
    yield SelectableOptionsFile(tmpfile)


class TestSelectableOptionsFile:

    @pytest.mark.parametrize(
        'content,selected', [('foo [bar] baz', 'bar'), ('foo bar baz', None)])
    def test_selected(self, select_file, tmpfile, content, selected):
        """The selected option is returned or None if nothing is selected."""
        tmpfile.write_text(content)
        assert select_file.selected == selected

    def test_select(self, select_file, tmpfile):
        """The specified option can be selected."""
        tmpfile.write_text('foo [bar] baz')
        select_file.select('baz')
        # The value is written to file. For /proc and /sys files this will
        # result in passing the value to the kernel.
        assert tmpfile.read_text() == 'baz'

    def test_select_invalid(self, select_file, tmpfile):
        """If an invalid value is specified, a ValueError is raised."""
        tmpfile.write_text('foo [bar] baz')
        with pytest.raises(ValueError):
            select_file.select('unknown')


@pytest.fixture
def toggle_options_file(tmpfile):
    yield TogglableOptionsFile(tmpfile)


class TestTogglableOptionsFile:

    def test_options(self, toggle_options_file, tmpfile):
        """Options are returned as a dict with current values."""
        tmpfile.write_text('foo\nnobar\nbaz')
        assert toggle_options_file.options == {
            'foo': True,
            'bar': False,
            'baz': True
        }

    @pytest.mark.parametrize(
        'value,content', [(True, 'bar'), (False, 'nobar')])
    def test_toggle_option(self, toggle_options_file, tmpfile, value, content):
        """Options can be toggled."""
        tmpfile.write_text('foo\nnobar\nbaz')
        toggle_options_file.toggle('bar', value)
        # The value is written to file. For /proc and /sys files this will
        # result in passing the value to the kernel.
        assert tmpfile.read_text() == content

    def test_toggle_option_unknown(self, toggle_options_file, tmpfile):
        """Passing an unknown option name raises a ValueError."""
        tmpfile.write_text('foo\nnobar\nbaz')
        with pytest.raises(ValueError):
            toggle_options_file.toggle('other', True)


@pytest.fixture
def value_file(tmpfile):
    yield ValueFile(tmpfile)


class TestValueFile:

    def test_value(self, value_file, tmpfile):
        """Value from the file can be returned."""
        tmpfile.write_text('55\n')
        assert value_file.value == '55'

    def test_set(self, value_file, tmpfile):
        """Value can be set to file."""
        value_file.set('99')
        assert tmpfile.read_text() == '99'


@pytest.fixture
def toggle_file(tmpfile):
    yield ToggleFile(tmpfile)


class TestToggleFile:

    @pytest.mark.parametrize(
        'content,enabled', [('1\n', True), ('0\n', False)])
    def test_enabled(self, toggle_file, tmpfile, content, enabled):
        """The enabled value can be returned."""
        tmpfile.write_text(content)
        assert toggle_file.enabled == enabled

    @pytest.mark.parametrize('enabled,content', [(True, '1'), (False, '0')])
    def test_toggl(self, toggle_file, tmpfile, enabled, content):
        """The value can be toggled."""
        toggle_file.toggle(enabled)
        assert toggle_file.enabled == enabled
        assert tmpfile.read_text() == content

#
# This file is part of LxStats.
#
# LxStats is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# LxStats is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# LxStats.  If not, see <http://www.gnu.org/licenses/>.

from ...testing import TestCase
from ..types import (
    OptionsFile, SelectableOptionsFile, TogglableOptionsFile, ValueFile,
    ToggleFile)


class OptionsFileTests(TestCase):

    def setUp(self):
        super().setUp()
        self.filename = 'file'
        self.options_file = OptionsFile(self.tempdir.join(self.filename))

    def test_options_single_line(self):
        '''Option values can be listed from single-line files.'''
        self.tempdir.mkfile(path=self.filename, content='foo bar baz')
        self.assertEqual(self.options_file.options, ['foo', 'bar', 'baz'])

    def test_options_multiple_lines(self):
        '''Option values can be listed from multi-lines files.'''
        self.tempdir.mkfile(path=self.filename, content='foo\nbar\nbaz')
        self.assertEqual(self.options_file.options, ['foo', 'bar', 'baz'])

    def test_options_selected(self):
        '''The selected option is included.'''
        self.tempdir.mkfile(path=self.filename, content='foo [bar] baz')
        self.assertEqual(self.select_file.options, ['foo', 'bar', 'baz'])


class SelectableOptionsFileTests(TestCase):

    def setUp(self):
        super().setUp()
        self.filename = 'file'
        self.select_file = SelectableOptionsFile(
            self.tempdir.join(self.filename))

    def test_selected(self):
        '''The selected option can be returned.'''
        self.tempdir.mkfile(path=self.filename, content='foo [bar] baz')
        self.assertEqual(self.select_file.selected, 'bar')

    def test_selected_none(self):
        '''None is returned if no option is selected.'''
        self.tempdir.mkfile(path=self.filename, content='foo bar baz')
        self.assertIsNone(self.select_file.selected)

    def test_select(self):
        '''The specified option can be selected.'''
        self.tempdir.mkfile(path=self.filename, content='foo [bar] baz')
        self.select_file.select('baz')
        # The value is written to file. For /proc and /sys files this will
        # result in passing the value to the kernel.
        self.assertEqual(
            self.readfile(self.tempdir.join(self.filename)), 'baz')

    def test_select_invalid(self):
        '''If an invalid value is specified, a ValueError is raised.'''
        self.tempdir.mkfile(path=self.filename, content='foo [bar] baz')
        self.assertRaises(ValueError, self.select_file.select, 'unknown')


class TogglableOptionsFileTests(TestCase):

    def setUp(self):
        super().setUp()
        self.filename = 'file'
        self.toggle_options_file = TogglableOptionsFile(
            self.tempdir.join(self.filename))

    def test_options(self):
        '''Options are returned as a dict with current values.'''
        self.tempdir.mkfile(path=self.filename, content='foo\nnobar\nbaz')
        self.assertEqual(
            self.toggle_options_file.options,
            {'foo': True, 'bar': False, 'baz': True})

    def test_toggle_option_true(self):
        '''Options can be enabled.'''
        self.tempdir.mkfile(path=self.filename, content='foo\nnobar\nbaz')
        self.toggle_options_file.toggle('bar', True)
        # The value is written to file. For /proc and /sys files this will
        # result in passing the value to the kernel.
        self.assertEqual(
            self.readfile(self.tempdir.join(self.filename)), 'bar')

    def test_toggle_option_false(self):
        '''Options can be disabled.'''
        self.tempdir.mkfile(path=self.filename, content='foo\nnobar\nbaz')
        self.toggle_options_file.toggle('foo', False)
        # When an option is disabled the name is prefixed with 'no'.
        self.assertEqual(
            self.readfile(self.tempdir.join(self.filename)), 'nofoo')

    def test_toggle_option_unknown(self):
        '''Passing an unknown option name raises a ValueError.'''
        self.tempdir.mkfile(path=self.filename, content='foo\nnobar\nbaz')
        self.assertRaises(
            ValueError, self.toggle_options_file.toggle, 'other', True)


class ValueFileTests(TestCase):

    def setUp(self):
        super().setUp()
        self.filename = 'file'
        self.value_file = ValueFile(self.tempdir.join(self.filename))

    def test_value(self):
        '''Value from the file can be returned.'''
        self.tempdir.mkfile(path=self.filename, content='55\n')
        self.assertEqual(self.value_file.value, '55')

    def test_set(self):
        '''Value can be set to file.'''
        self.value_file.set('99')
        self.assertEqual(self.readfile(self.tempdir.join(self.filename)), '99')


class ToggleFileTests(TestCase):

    def setUp(self):
        super().setUp()
        self.filename = 'file'
        self.toggle_file = ToggleFile(self.tempdir.join(self.filename))

    def test_enabled_true(self):
        '''If content is '1', the toggle is enabled.'''
        self.tempdir.mkfile(path=self.filename, content='1\n')
        self.assertTrue(self.toggle_file.enabled)

    def test_enabled_false(self):
        '''If content is '0', the toggle is not enabled.'''
        self.tempdir.mkfile(path=self.filename, content='0\n')
        self.assertFalse(self.toggle_file.enabled)

    def test_toggle_true(self):
        '''The value can be set to enabled.'''
        self.toggle_file.toggle(True)
        self.assertTrue(self.toggle_file.enabled)
        self.assertEqual(self.readfile(self.tempdir.join(self.filename)), '1')

    def test_toggle_false(self):
        '''The value can be set to disabled.'''
        self.toggle_file.toggle(False)
        self.assertFalse(self.toggle_file.enabled)
        self.assertEqual(self.readfile(self.tempdir.join(self.filename)), '0')

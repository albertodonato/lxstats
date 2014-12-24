from procsys.testing import TestCase

from procsys.files import OptionSelectFile, ToggleFile


class OptionSelectFileTests(TestCase):

    def setUp(self):
        super(OptionSelectFileTests, self).setUp()
        self.path = self.mktemp()
        self.select_file = OptionSelectFile(self.path)

    def test_options(self):
        '''Option values can be listed.'''
        self.mkfile(path=self.path, content='foo bar baz')
        self.assertEqual(self.select_file.options, ['foo', 'bar', 'baz'])

    def test_options_selected(self):
        '''The selected option is included.'''
        self.mkfile(path=self.path, content='foo [bar] baz')
        self.assertEqual(self.select_file.options, ['foo', 'bar', 'baz'])

    def test_selected(self):
        '''The selected option can be returned.'''
        self.mkfile(path=self.path, content='foo [bar] baz')
        self.assertEqual(self.select_file.selected, 'bar')

    def test_selected_none(self):
        '''None is returned if no option is selected.'''
        self.mkfile(path=self.path, content='foo bar baz')
        self.assertIsNone(self.select_file.selected)

    def test_select(self):
        '''The specified option can be selected.'''
        self.mkfile(path=self.path, content='foo [bar] baz')
        self.select_file.select('baz')
        # The value is written to file. For /proc and /sys files this will
        # result in passing the value to the kernel.
        self.assertEqual(self.readfile(self.path), 'baz')

    def test_select_invalid(self):
        '''If an invalid value is specified, a ValueError is raised.'''
        self.mkfile(path=self.path, content='foo [bar] baz')
        self.assertRaises(ValueError, self.select_file.select, 'unknown')


class ToggleFileTests(TestCase):

    def setUp(self):
        super(ToggleFileTests, self).setUp()
        self.path = self.mktemp()
        self.toggle_file = ToggleFile(self.path)

    def test_enabled_true(self):
        '''If content is '1', the toggle is enabled.'''
        self.mkfile(path=self.path, content='1\n')
        self.assertTrue(self.toggle_file.enabled)

    def test_enabled_false(self):
        '''If content is '0', the toggle is not enabled.'''
        self.mkfile(path=self.path, content='0\n')
        self.assertFalse(self.toggle_file.enabled)

    def test_toggle_true(self):
        '''The value can be set to enabled.'''
        self.toggle_file.toggle(True)
        self.assertTrue(self.toggle_file.enabled)
        self.assertEqual(self.readfile(self.path), '1')

    def test_toggle_false(self):
        '''The value can be set to disabled.'''
        self.toggle_file.toggle(False)
        self.assertFalse(self.toggle_file.enabled)
        self.assertEqual(self.readfile(self.path), '0')

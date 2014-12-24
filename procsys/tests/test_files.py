from procsys.testing import TestCase

from procsys.files import ToggleFile


class ToggleFileTests(TestCase):

    def setUp(self):
        super(ToggleFileTests, self).setUp()
        self.path = self.mktemp()
        self.toggle_file = ToggleFile(self.path)

    def test_options(self):
        '''Option values can be listed.'''
        self.mkfile(path=self.path, content='foo bar baz')
        self.assertEqual(self.toggle_file.options, ['foo', 'bar', 'baz'])

    def test_options_selected(self):
        '''The selected option is included.'''
        self.mkfile(path=self.path, content='foo [bar] baz')
        self.assertEqual(self.toggle_file.options, ['foo', 'bar', 'baz'])

    def test_selected(self):
        '''The selected option can be returned.'''
        self.mkfile(path=self.path, content='foo [bar] baz')
        self.assertEqual(self.toggle_file.selected, 'bar')

    def test_selected_none(self):
        '''None is returned if no option is selected.'''
        self.mkfile(path=self.path, content='foo bar baz')
        self.assertIsNone(self.toggle_file.selected)

    def test_select(self):
        '''The specified option can be selected.'''
        self.mkfile(path=self.path, content='foo [bar] baz')
        self.toggle_file.select('baz')
        # The value is written to file. For /proc and /sys files this will
        # result in passing the value to the kernel.
        self.assertEqual(self.readfile(self.path), 'baz')

    def test_select_invalid(self):
        '''If an invalid value is specified, a ValueError is raised.'''
        self.mkfile(path=self.path, content='foo [bar] baz')
        self.assertRaises(ValueError, self.toggle_file.select, 'unknown')

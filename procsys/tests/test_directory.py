#
# This file is part of Procsys.

# Procsys is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Procsys is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Procsys.  If not, see <http://www.gnu.org/licenses/>.

from os import path

from procsys.testing import TestCase
from procsys.files import File
from procsys.directory import Directory


class DirectoryTests(TestCase):

    def setUp(self):
        super(DirectoryTests, self).setUp()
        self.path = self.mkdir()
        self.dir = Directory(self.path)
        self.dir.files = {'foo': File, 'bar': File}

    def test_list_specified(self):
        '''Only names listed among Directory.files are returned.'''
        self.mkfile(path=path.join(self.path, 'foo'))
        self.mkfile(path=path.join(self.path, 'bar'))
        self.mkfile(path=path.join(self.path, 'bza'))
        self.assertEqual(self.dir.list(), ['bar', 'foo'])

    def test_list_existing(self):
        '''Only existing files are included in the listing.'''
        self.mkfile(path=path.join(self.path, 'foo'))
        self.assertEqual(self.dir.list(), ['foo'])

    def test_get_file(self):
        '''File items can be accessed.'''
        self.mkfile(path=path.join(self.path, 'foo'), content='foo text')
        file_item = self.dir['foo']
        self.assertIsInstance(file_item, File)
        self.assertEqual(file_item.read(), 'foo text')

    def test_get_file_unknown(self):
        '''Accessing an unknown file name raises an error.'''
        self.assertRaises(KeyError, self.dir.__getitem__, 'unknown')

    def test_get_file_not_existing(self):
        '''Accessing a known file that doesn't exist raises an error.'''
        self.assertRaises(KeyError, self.dir.__getitem__, 'foo')

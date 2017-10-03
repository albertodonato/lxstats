import os

from ..testing import TestCase
from ..fs import Entity, File, Directory


class EntityTests(TestCase):

    def setUp(self):
        super().setUp()
        self.filename = 'file'
        self.entity = Entity(self.tempdir.join(self.filename))

    def test_path(self):
        """The Entity path attribute contains the absolute path."""
        self.assertEqual(
            self.entity.path, os.path.join(self.tempdir.path, self.filename))

    def test_exists_false(self):
        """The exists property is False if the entity doesn't exist."""
        self.assertFalse(self.entity.exists)

    def test_exists_true(self):
        """The exists property is True if the entity exists."""
        self.tempdir.mkfile(path=self.filename)
        self.assertTrue(self.entity.exists)

    def test_readable_false(self):
        """The readable property is False if the path is not readable."""
        self.tempdir.mkfile(self.filename, mode=0o200)
        self.assertFalse(self.entity.readable)

    def test_readable_true(self):
        """The readable property is True if the path is readable."""
        self.tempdir.mkfile(path=self.filename)
        self.assertTrue(self.entity.readable)

    def test_writable_false(self):
        """The writable property is False if the path is not writable."""
        self.tempdir.mkfile(path=self.filename, mode=0o400)
        self.assertFalse(self.entity.writable)

    def test_writable_true(self):
        """The writable property is True if the path is writable."""
        self.tempdir.mkfile(path=self.filename)
        self.assertTrue(self.entity.writable)


class FileTests(TestCase):

    def setUp(self):
        super().setUp()
        self.filename = 'foo'
        self.file = File(os.path.join(self.tempdir.path, self.filename))

    def test_read(self):
        """File content can be read."""
        self.tempdir.mkfile(path=self.filename, content='some content')
        self.assertEqual(self.file.read(), 'some content')

    def test_write(self):
        """Content can be written to file."""
        self.file.write('some content')
        self.assertEqual(self.readfile(self.file.path), 'some content')


class DirectoryTests(TestCase):

    def setUp(self):
        super().setUp()
        self.dir = Directory(self.tempdir.path)
        self.dir.files = {'foo': File, 'bar': File}

    def test_list_specified(self):
        """Only names listed among Directory.files are returned."""
        self.tempdir.mkfile(path='foo')
        self.tempdir.mkfile(path='bar')
        self.tempdir.mkfile(path='bza')
        self.assertEqual(self.dir.list(), ['bar', 'foo'])

    def test_list_existing(self):
        """Only existing files are included in the listing."""
        self.tempdir.mkfile(path='foo')
        self.assertEqual(self.dir.list(), ['foo'])

    def test_listdir(self):
        """All names in the directory are returned."""
        self.tempdir.mkfile(path='foo')
        self.tempdir.mkfile(path='bar')
        self.assertCountEqual(self.dir.listdir(), ['bar', 'foo'])

    def test_iterable(self):
        """The Directory is iterable and returns Files in the directory."""
        self.tempdir.mkfile(path='foo')
        self.tempdir.mkfile(path='bar')
        file_list = list(self.dir)
        for elem in file_list:
            self.assertIsInstance(elem, File)
        self.assertEqual([elem.name for elem in file_list], ['bar', 'foo'])

    def test_get_file(self):
        """File items can be accessed."""
        self.tempdir.mkfile(path='foo', content='foo text')
        file_item = self.dir['foo']
        self.assertIsInstance(file_item, File)
        self.assertEqual(file_item.read(), 'foo text')

    def test_get_file_unknown(self):
        """Accessing an unknown file name raises an error."""
        self.assertRaises(KeyError, self.dir.__getitem__, 'unknown')

    def test_get_file_not_existing(self):
        """Accessing a known file that doesn't exist raises an error."""
        self.assertRaises(KeyError, self.dir.__getitem__, 'foo')

    def test_get_directory(self):
        """A Directory can contains sub-Directories."""

        class SubDirectory(Directory):
            files = {'foo': File}

        self.tempdir.mkfile(
            path=os.path.join('subdir', 'foo'), content='foo text')
        self.dir.files = {'subdir': SubDirectory}
        # The directory shows in the parent list
        self.assertEqual(self.dir.list(), ['subdir'])
        # The file is accessible through the tree
        self.assertEqual(self.dir['subdir']['foo'].read(), 'foo text')

    def test_join(self):
        """It's possible to join a path with the Directory one."""
        self.assertEqual(
            self.dir.join('append', 'path'),
            os.path.join(self.tempdir.path, 'append', 'path'))

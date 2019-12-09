from pathlib import PosixPath

import pytest

from ..fs import (
    Directory,
    File,
    Path,
)


@pytest.fixture
def posix_path(tmpdir):
    yield PosixPath(tmpdir / "somefile")


@pytest.fixture
def path(tmpdir, posix_path):
    yield Path(posix_path)


class TestPath:
    def test_path(self, tmpdir, path, posix_path):
        """The Path._pathattribute contains the absolute path."""
        assert path._path == posix_path

    @pytest.mark.parametrize("exists", [True, False])
    def test_exists(self, tmpdir, path, posix_path, exists):
        """The exists property returns whether the file exists."""
        if exists:
            posix_path.touch()
        assert path.exists == exists

    @pytest.mark.parametrize("mode,readable", [(0o400, True), (0o200, False)])
    def test_readable(self, tmpdir, path, posix_path, mode, readable):
        """The readable property returns whether the file is readable."""
        posix_path.touch()
        posix_path.chmod(mode)
        assert path.readable == readable

    @pytest.mark.parametrize("mode,writable", [(0o200, True), (0o400, False)])
    def test_writable(self, tmpdir, path, posix_path, mode, writable):
        """The writable property returns whether the file is writable."""
        posix_path.touch()
        posix_path.chmod(mode)
        assert path.writable == writable


@pytest.fixture
def file(tmpdir, posix_path):
    yield File(posix_path)


class TestFile:
    def test_read(self, file, posix_path):
        """File content can be read."""
        posix_path.write_text("some content")
        assert file.read() == "some content"

    def test_write(self, file, posix_path):
        """Content can be written to file."""
        file.write("some content")
        assert posix_path.read_text() == "some content"


@pytest.fixture
def dir(tmpdir, posix_path):
    posix_path.mkdir()
    dir = Directory(posix_path)
    dir.files = {"foo": File, "bar": File}
    yield dir


class TestDirectory:
    def test_list_specified(self, dir, posix_path):
        """Only names listed among Directory.files are returned."""
        (posix_path / "foo").touch()
        (posix_path / "bar").touch()
        (posix_path / "baz").touch()
        assert dir.list() == ["bar", "foo"]

    def test_list_existing(self, dir, posix_path):
        """Only existing files are included in the listing."""
        (posix_path / "foo").touch()
        assert dir.list() == ["foo"]

    def test_listdir(self, dir, posix_path):
        """All names in the directory are returned."""
        (posix_path / "foo").touch()
        (posix_path / "bar").touch()
        assert sorted(dir.listdir()) == ["bar", "foo"]

    def test_iterable(self, dir, posix_path):
        """The Directory is iterable and returns Files in the directory."""
        (posix_path / "foo").touch()
        (posix_path / "bar").touch()
        file_list = list(dir)
        for elem in file_list:
            assert isinstance(elem, File)
        assert [elem.name for elem in file_list] == ["bar", "foo"]

    def test_get_file(self, dir, posix_path):
        """File items can be accessed."""
        (posix_path / "foo").write_text("foo text")
        file_item = dir["foo"]
        assert isinstance(file_item, File)
        assert file_item.read() == "foo text"

    def test_get_file_unknown(self, dir):
        """Accessing an unknown file name raises an error."""
        with pytest.raises(KeyError):
            dir["unknown"]

    def test_get_file_not_existing(self, dir):
        """Accessing a known file that doesn't exist raises an error."""
        with pytest.raises(KeyError):
            dir["foo"]

    def test_get_directory(self, dir, posix_path):
        """A Directory can contains sub-Directories."""

        class SubDirectory(Directory):
            files = {"foo": File}

        dir.files = {"subdir": SubDirectory}
        (posix_path / "subdir").mkdir()
        (posix_path / "subdir" / "foo").write_text("foo text")
        # The directory shows in the parent list
        assert dir.list() == ["subdir"]
        # The file is accessible through the tree
        assert dir["subdir"]["foo"].read() == "foo text"

    def test_join(self, dir, posix_path):
        """It's possible to join a path with the Directory one."""
        assert dir.join("append", "path") == posix_path / "append" / "path"

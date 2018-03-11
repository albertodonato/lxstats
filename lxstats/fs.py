"""Files and directories access.

The :class:`File` and :class:`Directory` classes provide abstractions to access
filesytem entities.

"""

import os
from pathlib import PosixPath


class Path:
    """A filesystem path such as a file or directory."""

    def __init__(self, path):
        self._path = PosixPath(path).absolute()

    @property
    def name(self):
        return self._path.name

    @property
    def exists(self):
        """Whether the path exists."""
        return self._path.exists()

    @property
    def readable(self):
        """Whether the path is readable."""
        return os.access(str(self._path), os.R_OK)

    @property
    def writable(self):
        """Whether the path is writable."""
        return os.access(str(self._path), os.W_OK)


class File(Path):
    """Wrapper to reaad/write a file."""

    def read(self):
        """Return file content."""
        return self._path.read_text()

    def write(self, content):
        """Write content to file, replacing the content if it exists."""
        self._path.write_text(content)


class Directory(Path):
    """Access  files in a directory with a :class:`dict`-like interface."""

    #: Map names of files under the directory to their corresponding
    #: :class:`File` type.  Subclasses should define this.
    files = {}

    def list(self):
        """Return a list of names in the directory.

        Only existing files that match names listed in `files` are returned.

        """
        return sorted(
            name for name in self.files if (self._path / name).exists())

    def listdir(self):
        """Return all existing names in a directory."""
        return [path.name for path in self._path.iterdir()]

    def join(self, *paths):
        """Append the given path to the directory one."""
        return self._path.joinpath(*paths)

    def __getitem__(self, name):
        """Return the :class:`File` instance for a name."""
        item = self.files[name](self._path / name)
        if not item.exists:
            raise KeyError(name)
        return item

    def __iter__(self):
        """Return an iterator yielding :class:`File`s in the directory."""
        for name in self.list():
            yield self[name]

"""Files and directories access.

The :class:`File` and :class:`Directory` classes provide abstractions to access
filesytem entities.

"""

import os


class Entity:
    """A filesystem entity such as a file or directory."""

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path)

    @property
    def exists(self):
        """Whether the path exists."""
        return os.path.exists(self.path)

    @property
    def readable(self):
        """Whether the path is readable."""
        return os.access(self.path, os.R_OK)

    @property
    def writable(self):
        """Whether the path is writable."""
        return os.access(self.path, os.W_OK)


class File(Entity):
    """Wrapper to reaad/write a file."""

    def read(self):
        """Return file content."""
        with open(self.path) as fh:
            return fh.read()

    def write(self, content):
        """Write content to file, replacing the content if it exists."""
        with open(self.path, 'w') as fh:
            fh.write(content)


class Directory(Entity):
    """Access  files in a directory with a :class:`dict`-like interface."""

    #: Map names of files under the directory to their corresponding
    #: :class:`File` type.  Subclasses should define this.
    files = {}

    def list(self):
        """Return a list of names in the directory.

        Only existing files that match names listed in `files` are returned.

        """
        return sorted(
            name for name in self.files if os.path.exists(self._path(name)))

    def listdir(self):
        """Return all existing names in a directory."""
        return os.listdir(self.path)

    def join(self, *paths):
        """Append the given path to the directory one."""
        return os.path.join(self.path, *paths)

    def __getitem__(self, name):
        """Return the :class:`File` instance for a name."""
        path = self._path(name)
        item = self.files[name](path)
        if not item.exists:
            raise KeyError(name)
        return item

    def __iter__(self):
        """Return an iterator yielding :class:`File`s in the directory."""
        for name in self.list():
            yield self[name]

    def _path(self, name):
        return os.path.join(self.path, name)

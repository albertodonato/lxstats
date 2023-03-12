"""Files and directories access.

The :class:`File` and :class:`Directory` classes provide abstractions to access
filesytem entities.

"""

from collections.abc import Iterable
import os
import pathlib
from typing import (
    Any,
    ClassVar,
)


class Path:
    """A filesystem path such as a file or directory."""

    def __init__(self, path: str | pathlib.PurePath):
        self._path = pathlib.PosixPath(path).absolute()

    @property
    def name(self) -> str:
        return self._path.name

    @property
    def exists(self) -> bool:
        """Whether the path exists."""
        return self._path.exists()

    @property
    def readable(self) -> bool:
        """Whether the path is readable."""
        return os.access(str(self._path), os.R_OK)

    @property
    def writable(self) -> bool:
        """Whether the path is writable."""
        return os.access(str(self._path), os.W_OK)


class File(Path):
    """Wrapper to reaad/write a file."""

    def read(self) -> str:
        """Return file content."""
        return self._path.read_text()

    def write(self, content: str):
        """Write content to file, replacing the content if it exists."""
        self._path.write_text(content)


class Directory(Path):
    """Access  files in a directory with a :class:`dict`-like interface."""

    #: Map names of files under the directory to their corresponding
    #: :class:`File` type.
    #:
    #: Subclasses should define this.
    files: ClassVar[dict[str, type[Path]]] = {}

    def listdir(self) -> list[str]:
        """Return all existing names in a directory."""
        return [path.name for path in self._path.iterdir()]

    def join(self, *paths: str | pathlib.PurePath):
        """Append the given path to the directory one."""
        return self._path.joinpath(*paths)

    def list(self) -> list[str]:
        """Return a list of names in the directory.

        Only existing files that match names listed in `files` are returned.

        """
        return sorted(
            name for name in self.files if (self._path / name).exists()
        )

    def __getitem__(self, name: str) -> Any:
        """Return the :class:`File` instance for a name."""
        item = self.files[name](self._path / name)
        if not item.exists:
            raise KeyError(name)
        return item

    def __iter__(self) -> Iterable:
        """Return an iterator yielding :class:`File`s in the directory."""
        for name in self.list():
            yield self[name]

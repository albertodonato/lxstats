"""Classes for directory content."""

from abc import (
    ABCMeta,
    abstractmethod,
)

from ..fs import Directory


class ParsedDirectory(Directory, metaclass=ABCMeta):
    """A directory whose file listing is parsed."""

    def parse(self):
        """Return a parsed list of files in the directory."""
        if not self.exists:
            return

        return [self._parse(path) for path in self.listdir()]

    @abstractmethod
    def _parse(self, path):
        """Parse details for a path in the directory.

        .. note::
            Subclasses must implement this method.

        """

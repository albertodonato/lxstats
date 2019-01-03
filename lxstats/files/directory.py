"""Classes for directory content."""

from abc import (
    ABCMeta,
    abstractmethod,
)
from pathlib import Path
from typing import (
    Any,
    Dict,
    Optional,
)

from ..fs import Directory


class ParsedDirectory(Directory, metaclass=ABCMeta):
    """A directory whose file listing is parsed."""

    def parse(self) -> Optional[Dict[str, Any]]:
        """Return a dict with files in the directory and their parse result."""
        if not self.exists:
            return None

        return {path.name: self._parse(path) for path in self._path.iterdir()}

    @abstractmethod
    def _parse(self, path: Path):
        """Parse details for a path in the directory.

        .. note::
            Subclasses must implement this method.

        """

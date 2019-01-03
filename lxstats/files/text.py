"""Base classes for reading and parsing text files."""

from abc import (
    ABCMeta,
    abstractmethod,
)
from collections import Callable
from typing import Optional

from ..fs import File


class ParsedFile(File, metaclass=ABCMeta):
    """A file whose content is parsed.

    It's intended to be subclassed to provide parsers for specific types of
    files.

    Subclasses must implement the :func:`_parse` method which is called with
    the content of the file and returns the parsed information.

    """

    def parse(self):
        """Read the file and preturn the parsed content."""
        if not self.exists:
            return

        return self._parse(self.read())

    @abstractmethod
    def _parse(self, content: str):
        """Parse the content of the file.

        .. note::
            Subclasses must implement this method.

        """


class SingleLineFile(ParsedFile):
    """A single-line file that can be split into fields.

    The line is split into fields based on a :attr:`separator` (space by
    default).

    If the separator is set to None, the stripped content of the file is
    returned.

    If separator is a callable, it's used to split the field (it's called with
    the line and must return a list of fields).

    Subclasses can define a list of :attr:`fields` and a different
    :attr:`separator`.

    """

    #: The separator to use when splitting the content. If set to :data:`None`,
    #: content is not split.  It can also be set to a `callable` that splits
    #: content.
    separator: Optional[str] = ' '

    #: If set, it must be a list, where each element can be
    #:
    #: - a string: the key to use for the value.
    #: - a list of (key, type) tuples:  the value is  converted to the type by
    #:   calling :samp:`type(value)`.
    #: - :data:`None`: the field is ignored.
    fields = None

    def _parse(self, content):
        # Take just fhe first line
        content = content.split('\n')[0]
        if self.separator is None:
            return content

        splitted = self._split(content)
        if self.fields is None:
            return splitted

        fields = self._get_fields()

        # Map fields values to their name converting to the proper type
        return {
            key: field_type(value)
            for (key, field_type), value in zip(fields, splitted)
            if key is not None
        }

    def _get_fields(self):
        fields = []
        for field in self.fields:
            if field is None:
                field = (None, None)
            elif isinstance(field, str):
                field = (field, str)

            fields.append(field)
        return fields

    def _split(self, content):
        if not content:
            return []

        if isinstance(self.separator, Callable):
            return self.separator(content)

        content = content.strip(self.separator)
        return content.split(self.separator)


class SplittedFile(ParsedFile):
    """A file that is parsed by splitting the content in words.

    It's meant to work with files that have one word per line or a single
    space-separated line.

    Example of content::

      foo
      bar
      baz

    or::

      foo bar baz

    In both cases the result is :samp:`['foo', 'bar', 'baz']`.

    """

    def _parse(self, content):
        lines = content.splitlines()
        if len(lines) == 1:
            return lines[0].split()
        else:
            return lines

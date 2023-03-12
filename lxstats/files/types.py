"""Parse types of files used in /proc and /sys filesytems."""

from collections import OrderedDict
from typing import (
    cast,
    Optional,
)

from .text import (
    SingleLineFile,
    SplittedFile,
)


class OptionsFile(SplittedFile):
    """File listing a set of options.

    It returns available options for a file, including the selected one, if
    present.

    For example, for a file containing::

      foo [bar] baz

    :meth:`options` returns::

      ['foo', 'bar', 'baz']

    """

    @property
    def options(self) -> list[str]:
        """Return a list with avalilable options."""
        return [self._strip_selected(value) for value in self.parse()]

    def _strip_selected(self, value: str) -> str:
        return value[1:-1] if value.startswith("[") else value


class SelectableOptionsFile(OptionsFile):
    """File listing a set of options with a single selected one.


    It works like :class:`OptionsFile`, but also allow getting and setting the
    selected option.

    """

    @property
    def selected(self) -> str | None:
        """Return the selected option."""
        for value in self.parse():
            if value.startswith("["):
                return self._strip_selected(value)
        return None

    def select(self, value: str):
        """Set the specified option value.

        :class:`ValueError` is raised if the value is not valid."""

        if value not in self.options:
            raise ValueError(value)
        self.write(value)


class TogglableOptionsFile(OptionsFile):
    """A file with a list of options that can be individually enabled.

    Disabled options have names prefixed by :data:`no`.

    For example, for a file containing::

      foo
      nobar
      baz

    :meth:`options` returns::

      {'foo': True,
       'bar': False,
       'baz': True}

    """

    @property
    def options(self) -> dict[str, bool]:  # type: ignore
        """Return a dict with options and their current values."""
        options: dict[str, bool] = OrderedDict()
        for option in super().options:
            value = not option.startswith("no")
            if not value:
                option = option[2:]
            options[option] = value

        return options

    def toggle(self, option: str, value: bool):
        """Change the value of the specified option."""
        if option not in self.options:
            raise ValueError(option)

        prefix = "" if value else "no"
        self.write(f"{prefix}{option}")


class ValueFile(SingleLineFile):
    """File containing a single value that can be read or set."""

    separator = None

    @property
    def value(self) -> str | None:
        """Return the current value in the file."""
        return cast(Optional[str], self.parse())

    def set(self, value: str):
        self.write(value)


class ToggleFile(SingleLineFile):
    """File to enable or disable an option.

    The file contains a boolean value expressed as :data:`0` or :data:`1`.

    """

    separator = None

    @property
    def enabled(self) -> bool:
        """Return whether the toggle value is enabled."""
        return bool(self.parse() == "1")

    def toggle(self, value: bool):
        """Enable or disable the value based on the passed :class:`bool`."""
        content = "1" if value else "0"
        self.write(content)

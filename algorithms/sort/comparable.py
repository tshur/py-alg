from typing import Any, Protocol


class Comparable(Protocol):
    """An abstract class supporting < comparison for typing usage."""

    def __lt__(self, other: Any, /) -> bool: ...

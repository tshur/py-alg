from typing import Any, Protocol


class SupportsRichComparison(Protocol):
    """An abstract type interface supporting < (__lt__) comparison."""

    def __lt__(self, other: Any, /) -> bool: ...

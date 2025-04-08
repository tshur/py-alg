from abc import ABCMeta, abstractmethod
from typing import Any

class Comparable(metaclass=ABCMeta):
    """An abstract class supporting < comparison for typing usage."""

    @abstractmethod
    def __lt__(self, other: Any) -> bool: ...

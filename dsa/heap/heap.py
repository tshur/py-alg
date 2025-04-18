from typing import Iterable, Optional, Self

from dsa.typing.comparison import Comparable


class Heap[CT: Comparable]:
    def __init__(self):
        raise NotImplementedError

    @classmethod
    def from_iterable(cls, iterable: Iterable[CT]) -> Self:
        raise NotImplementedError

    def push(self, value: CT) -> None:
        raise NotImplementedError

    def pop(self) -> Optional[CT]:
        raise NotImplementedError

    def peek(self) -> Optional[CT]:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

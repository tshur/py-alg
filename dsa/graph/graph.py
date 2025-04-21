from abc import ABC, abstractmethod
from typing import Iterator, Self


class GraphBase[T](ABC):
    @classmethod
    def from_edges(cls, edges: list[tuple[T, T]]) -> Self:
        graph = cls()
        for edge in edges:
            graph.add_edge(edge)
        return graph

    @abstractmethod
    def add(self, node: T) -> None: ...

    @abstractmethod
    def remove(self, node: T) -> None: ...

    @abstractmethod
    def add_edge(self, edge: tuple[T, T]) -> None: ...

    @abstractmethod
    def remove_edge(self, edge: tuple[T, T]) -> None: ...

    @abstractmethod
    def has_edge(self, edge: tuple[T, T]) -> bool: ...

    @abstractmethod
    def __iter__(self) -> Iterator[T]: ...

    @abstractmethod
    def bfs_iterator(self, start: T) -> Iterator[T]: ...

    @abstractmethod
    def dfs_iterator(self, start: T) -> Iterator[T]: ...

    def __contains__(self, value: T) -> bool:
        return value in iter(self)

    @abstractmethod
    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        return len(self) > 0

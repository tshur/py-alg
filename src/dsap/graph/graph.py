from abc import ABC, abstractmethod
from typing import Iterable, Iterator, Self


class GraphBase[T](ABC):
    @classmethod
    def from_edges(cls, edges: Iterable[tuple[T, T]]) -> Self:
        """Build a graph from an iterable of edges.

        The graph will be created by repeatedly calling add_edge(edge). Edges will be
        added in order, and nodes will be added as necessary.

        Args:
            edges (Iterable[tuple[T, T]]): An iterable of directional (from, to) pairs.
              The edges will be added to the graph.

        Returns:
            Self: The newly constructed graph.
        """
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
        """Return if a given value exists in the graph.

        This checks for node containment only: the linking of edges is irrelevant to
        whether or not a node is in the graph (except that a node always exists if an
        edge from/to it exists).

        Args:
            value (T): The value to search for in the graph.

        Returns:
            bool: True if the node value is in the graph. False, otherwise.
        """
        return value in iter(self)

    @abstractmethod
    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Returns true if the graph has at least one node in it.

        Returns:
            bool: True if the graph has at least one node in it. False, otherwise.
        """
        return len(self) > 0

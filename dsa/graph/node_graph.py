from typing import Iterator

from dsa.graph.graph import GraphBase
from dsa.queue.queue import Queue
from dsa.stack.stack import Stack


class NodeGraph[T](GraphBase[T]):
    _nodes: dict[T, list[T]]

    def __init__(self):
        self._nodes = {}

    def add(self, node: T) -> None:
        if node not in self._nodes:
            self._nodes[node] = []

    def remove(self, node: T) -> None:
        if node not in self._nodes:
            return
        for other in self:
            self.remove_edge((other, node))
        del self._nodes[node]

    def add_edge(self, edge: tuple[T, T]) -> None:
        self.add(edge[0])
        self.add(edge[1])
        self._nodes[edge[0]].append(edge[1])

    def remove_edge(self, edge: tuple[T, T]) -> None:
        if edge[0] not in self._nodes:
            return
        try:
            self._nodes[edge[0]].remove(edge[1])
        except ValueError:
            pass  # Edge not found, this is OK.

    def has_edge(self, edge: tuple[T, T]) -> bool:
        return edge[0] in self._nodes and edge[1] in self._nodes[edge[0]]

    def __iter__(self) -> Iterator[T]:
        yield from self._nodes.keys()

    def bfs_iterator(self, start: T) -> Iterator[T]:
        if start not in self._nodes:
            return

        seen = set[T]()
        queue = Queue[T].from_iterable([start])
        while queue:
            node = queue.dequeue()
            if node is None or node in seen:
                continue
            seen.add(node)

            yield node
            for neighbor in self._nodes[node]:
                queue.enqueue(neighbor)

    def dfs_iterator(self, start: T) -> Iterator[T]:
        if start not in self._nodes:
            return

        seen = set[T]()
        stack = Stack[T].from_iterable([start])
        while stack:
            node = stack.pop()
            if node is None or node in seen:
                continue
            seen.add(node)

            yield node
            for neighbor in self._nodes[node]:
                stack.push(neighbor)

    def __len__(self) -> int:
        return len(self._nodes)

    def __str__(self) -> str:
        out: list[str] = []
        for node in iter(self):
            out.append(f"{node} -> {self._nodes[node]}")
        return "\n".join(out)

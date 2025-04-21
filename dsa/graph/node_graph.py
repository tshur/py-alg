from typing import Iterator

from dsa.graph.graph import GraphBase
from dsa.queue.queue import Queue
from dsa.stack.stack import Stack


class NodeGraph[T](GraphBase[T]):
    """Graph data structure implemented using a mapping of {node: set[node]}.

    We directly hash the value T as a node, and do not add any extra class / object
    overhead. Therefore, the value T type must be hashable. We aggregate edges into a
    set for faster lookup.

    Basic operations: (V is number of nodes, E is number of edges)
      - add, O(1)
      - remove, O(1)
      - add_edge, O(1)
      - remove_edge, O(V)
      - has_edge, O(1)
      - __iter__, O(V)
      - bfs_iterator, O(V + E)
      - dfs_iterator, O(V + E)
    """

    _nodes: dict[T, set[T]]

    def __init__(self):
        self._nodes = {}

    def add(self, node: T) -> None:
        if node not in self._nodes:
            self._nodes[node] = set()

    def remove(self, node: T) -> None:
        if node not in self._nodes:
            return
        for other in self:
            self.remove_edge((other, node))
        del self._nodes[node]

    def add_edge(self, edge: tuple[T, T]) -> None:
        self.add(edge[0])
        self.add(edge[1])
        self._nodes[edge[0]].add(edge[1])

    def remove_edge(self, edge: tuple[T, T]) -> None:
        if edge[0] not in self._nodes:
            return
        try:
            self._nodes[edge[0]].remove(edge[1])
        except KeyError:
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
            out.append(f"{node} -> {list(self._nodes[node])}")
        return "\n".join(out)

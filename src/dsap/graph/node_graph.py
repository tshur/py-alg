from typing import Iterator

from dsap.hash import Map, Set
from dsap.queue import Queue
from dsap.sort import sort
from dsap.stack import Stack

from .graph import GraphBase


class NodeGraph[T](GraphBase[T]):
    """Graph data structure implemented using an adjacency list of {node: Set[node]}.

    We directly hash the value T as a node, and do not add any extra class / object
    overhead. Therefore, the value T type must be hashable. We aggregate edges into a
    set for faster lookup. Other design options are list[node] (unsorted / sorted) and
    LinkedList[node].

    Basic operations: (V is number of nodes, E is number of edges)
      - add, O(1)
      - remove, O(V)
      - add_edge, O(1)
      - remove_edge, O(1)
      - has_edge, O(1)
      - __iter__, O(V)
      - bfs_iterator, O(V + E)
      - dfs_iterator, O(V + E)
    """

    _nodes: Map[T, Set[T]]

    def __init__(self):
        self._nodes = Map()

    def add(self, node: T) -> None:
        """Add a new (empty) node into the graph. Does not create any edges.

        If the node already exists, this does nothing.

        Args:
            node (T): The node value to add.

        Examples:
            >>> graph = NodeGraph()
            >>> graph.add(1)
            >>> graph.add(2)
            >>> len(graph)
            2
        """
        if node not in self._nodes:
            self._nodes[node] = Set()

    def remove(self, node: T) -> None:
        """Remove a node (and all edges to/from it) from the graph.

        If the node does not exist, this function does nothing. Part of removing a node
        means we must find all edges to/from the node and delete them (otherwise, they
        will reference a missing node!).

        Complexity:
            Time: O(V), due to having to remove inbound edges to the removed node.
              Requires checking all the other nodes in O(1) time each (due to set).

        Args:
            node (T): The node value to remove.

        Examples:
            >>> graph = NodeGraph().from_edges([(1, 2), (2, 2)])
            >>> graph.remove((1, 2))
            >>> graph.remove((2, 2))
            >>> graph.remove((3, 4))
            >>> len(graph)
            2
        """
        if node not in self._nodes:
            return
        for other in self:
            self.remove_edge((other, node))
        del self._nodes[node]

    def add_edge(self, edge: tuple[T, T]) -> None:
        """Add a (from, to) edge pair to the graph.

        Both from and to nodes will be added if they are not already part of the graph.

        Args:
            edge (tuple[T, T]): The edge to be added.

        Examples:
            >>> graph = NodeGraph()
            >>> graph.add_edge((1, 2))
            >>> graph.has_edge((1, 2))
            True
            >>> 1 in graph
            True
        """
        self.add(edge[0])
        self.add(edge[1])
        self._nodes[edge[0]].add(edge[1])

    def remove_edge(self, edge: tuple[T, T]) -> None:
        """Remove an edge from the graph (if it exists).

        If the edge does not exist, the graph will not be affected. Even if a removed
        edge causes a node to have no remaining neighbors, that node will still remain
        in the graph (unless it is specifically removed).

        Args:
            edge (tuple[T, T]): The edge to be removed, given as (from, to) pair.

        Examples:
            >>> graph = NodeGraph().from_edges([(1, 2), (2, 2), (3, 4)])
            >>> graph.remove_edge((3, 4))
            >>> graph.has_edge((3, 4))
            False
            >>> 4 in graph
            True
        """
        try:
            self._nodes[edge[0]].remove(edge[1])
        except KeyError:
            pass  # Edge not found, this is OK.

    def has_edge(self, edge: tuple[T, T]) -> bool:
        """Whether the graph has a given (from, to) edge between two nodes.

        Args:
            edge (tuple[T, T]): The edge to check for.

        Returns:
            bool: True if the connection (from, to) exists in the graph. False,
              otherwise.

        Examples:
            >>> graph = NodeGraph().from_edges([(1, 2), (3, 4)])
            >>> graph.has_edge((3, 4))
            True
            >>> graph.has_edge((1, 1))
            False
        """
        return edge[0] in self._nodes and edge[1] in self._nodes[edge[0]]

    def __iter__(self) -> Iterator[T]:
        """Yields an iterator over node values in the graph.

        Complexity:
            Time: O(V), since we have access to each node value without a BFS/DFS
              traversal over the graph.

        Yields:
            Iterator[T]: Nodes in the graph.

        Examples:
            >>> graph = NodeGraph().from_edges([(1, 2), (3, 4)])
            >>> list(graph)
            [1, 2, 3, 4]
        """
        yield from self._nodes.keys()

    def bfs_iterator(self, start: T) -> Iterator[T]:
        """Breadth-first search iterator over nodes in the graph from a given start.

        Using a queue, we can traverse the graph from some starting point in BFS manner.
        For each node, we will visit its neighbors before visiting deeper descendents in
        the graph.

        Unconnected components will not be visited, because the search will start from
        the given node, which may not connect to all nodes in the graph. Cycles are
        handled.

        Complexity:
            Time: O(V + E), due to having to travel (at worst case) all nodes and edges.

        Args:
            start (T): The node to start the BFS traversal from.

        Yields:
            Iterator[T]: Nodes visited in BFS order (starting with the given node).

        Examples:
            >>> graph = NodeGraph().from_edges([(1, 2), (2, 3), (3, 3)])
            >>> list(graph.bfs_iterator(1))
            [1, 2, 3]
            >>> list(graph.bfs_iterator(3))
            [3]
        """
        if start not in self._nodes:
            return

        seen = Set[T]()
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
        """Depth-first search iterator over nodes in the graph from a given start.

        Using a stack, we can traverse the graph from some starting point in DFS manner.
        For each node, we will traverse edges as deeply as possible before visiting
        other neighbors in the graph.

        Unconnected components will not be visited, because the search will start from
        the given node, which may not connect to all nodes in the graph. Cycles are
        handled.

        Complexity:
            Time: O(V + E), due to having to travel (at worst case) all nodes and edges.

        Args:
            start (T): The node to start the DFS traversal from.

        Yields:
            Iterator[T]: Nodes visited in DFS order (starting with the given node).

        Examples:
            >>> graph = NodeGraph().from_edges([(1, 2), (2, 3), (3, 3)])
            >>> list(graph.dfs_iterator(1))
            [1, 2, 3]
            >>> list(graph.dfs_iterator(3))
            [3]
        """
        if start not in self._nodes:
            return

        seen = Set[T]()
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
        """Returns the number of nodes in the graph.

        Returns:
            int: The number of nodes in the graph.

        Examples:
            >>> graph = NodeGraph().from_edges([(1, 2), (2, 2), (3, 4)])
            >>> len(graph)
            4
        """
        return len(self._nodes)

    def __str__(self) -> str:
        """Returns a printable display of the adjacency list graph structure.

        Since the graph is internally implemented with a dict of sets, do not rely on
        the ordering of the str output! The ordering of neighbors is non-deterministic.

        Returns:
            str: The printable representation of the graph.

        Examples:
            >>> graph = NodeGraph().from_edges([(1, 2), (2, 3), (4, 4)])
            >>> print(graph)
            1 -> [2]
            2 -> [3]
            3 -> []
            4 -> [4]
        """
        out: list[str] = []
        for node in iter(self):
            out.append(f"{node} -> {list(self._nodes[node])}")
        return "\n".join(sort(out))

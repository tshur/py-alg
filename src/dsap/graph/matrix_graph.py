from typing import Iterable, Iterator, Self

from dsap.hash import Map, Set
from dsap.queue import Queue
from dsap.sort import sort
from dsap.stack import Stack
from .graph import GraphBase


class MatrixGraph[T](GraphBase[T]):
    """Graph data structure implemented using an adjacency matrix of {node: Set[node]}.

    We need extra mappings to convert each node to an int index into the matrix (and the
    inverse). Then, for each node i and node j, _matrix[i][j] represents an edge from i
    to j.

    Adjacency matrix works best if the matrix is dense, and we are not adding/removing
    nodes very often.

    Basic operations: (V is number of nodes, E is number of edges)
      - from_edges, O(V**2 + E)
      - add, O(V)
      - remove, O(V**2)
      - add_edge, O(1) if nodes in graph, otherwise O(V)
      - remove_edge, O(1)
      - has_edge, O(1)
      - __iter__, O(V)
      - bfs_iterator, O(V + E)
      - dfs_iterator, O(V + E)
    """

    _nodes: list[T]
    _node_to_id: Map[T, int]
    _matrix: list[list[bool]]

    def __init__(self):
        self._nodes = []
        self._node_to_id = Map()
        self._matrix = []

    @classmethod
    def from_edges(cls, edges: Iterable[tuple[T, T]]) -> Self:
        """Build a graph from an iterable of edges.

        We can more efficiently build a graph if we know all the edges / nodes in
        advance. Calling add(...) repeatedly is inefficient. Instead, we collect all
        nodes and build the matrix + mappings directly. Then, we can use add_edge to set
        the neighbor connections.

        Args:
            edges (Iterable[tuple[T, T]]): An iterable of directional (from, to) pairs.
              The edges will be added to the graph.

        Returns:
            Self: The newly constructed graph.
        """
        nodes = Set[T]()
        for source, destination in edges:
            nodes.add(source)
            nodes.add(destination)

        graph = cls()
        graph._nodes = list(nodes)
        graph._node_to_id = Map[T, int].from_items(
            (node, i) for i, node in enumerate(graph._nodes)
        )
        graph._matrix = [[False] * len(graph._nodes) for _ in range(len(graph._nodes))]
        for edge in edges:
            graph.add_edge(edge)
        return graph

    def add(self, node: T) -> None:
        """Add a new (empty) node into the graph. Does not create any edges.

        If the node already exists, this does nothing.

        Args:
            node (T): The node value to add.

        Examples:
            >>> graph = MatrixGraph()
            >>> graph.add(1)
            >>> graph.add(2)
            >>> len(graph)
            2
        """
        if node in self:
            return
        self._node_to_id[node] = len(self._nodes)
        self._nodes.append(node)
        for row in self._matrix:
            row.append(False)
        self._matrix.append([False for _ in range(len(self._nodes))])

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
            >>> graph = MatrixGraph().from_edges([(1, 2), (2, 2)])
            >>> graph.remove((1, 2))
            >>> graph.remove((2, 2))
            >>> graph.remove((3, 4))
            >>> len(graph)
            2
        """
        if node not in self:
            return

        node_id = self._node_to_id[node]
        del self._matrix[node_id]
        for row in self._matrix:
            del row[node_id]
        del self._nodes[node_id]
        del self._node_to_id[node]

        # Need to also re-map other nodes and their ids such that they are sequential.
        for other_id in range(node_id, len(self._nodes)):
            self._node_to_id[self._nodes[other_id]] = other_id

    def add_edge(self, edge: tuple[T, T]) -> None:
        """Add a (from, to) edge pair to the graph.

        Both from and to nodes will be added if they are not already part of the graph.

        Args:
            edge (tuple[T, T]): The edge to be added.

        Examples:
            >>> graph = MatrixGraph()
            >>> graph.add_edge((1, 2))
            >>> graph.has_edge((1, 2))
            True
            >>> 1 in graph
            True
        """
        self.add(edge[0])
        self.add(edge[1])
        self._matrix[self._node_to_id[edge[0]]][self._node_to_id[edge[1]]] = True

    def remove_edge(self, edge: tuple[T, T]) -> None:
        """Remove an edge from the graph (if it exists).

        If the edge does not exist, the graph will not be affected. Even if a removed
        edge causes a node to have no remaining neighbors, that node will still remain
        in the graph (unless it is specifically removed).

        Args:
            edge (tuple[T, T]): The edge to be removed, given as (from, to) pair.

        Examples:
            >>> graph = MatrixGraph().from_edges([(1, 2), (2, 2), (3, 4)])
            >>> graph.remove_edge((3, 4))
            >>> graph.has_edge((3, 4))
            False
            >>> 4 in graph
            True
        """
        if edge[0] not in self or edge[1] not in self:
            return

        self._matrix[self._node_to_id[edge[0]]][self._node_to_id[edge[1]]] = False

    def has_edge(self, edge: tuple[T, T]) -> bool:
        """Whether the graph has a given (from, to) edge between two nodes.

        Args:
            edge (tuple[T, T]): The edge to check for.

        Returns:
            bool: True if the connection (from, to) exists in the graph. False,
              otherwise.

        Examples:
            >>> graph = MatrixGraph().from_edges([(1, 2), (3, 4)])
            >>> graph.has_edge((3, 4))
            True
            >>> graph.has_edge((1, 1))
            False
        """
        if edge[0] not in self or edge[1] not in self:
            return False

        return self._matrix[self._node_to_id[edge[0]]][self._node_to_id[edge[1]]]

    def __iter__(self) -> Iterator[T]:
        """Yields an iterator over node values in the graph.

        Complexity:
            Time: O(V), since we have access to each node value without a BFS/DFS
              traversal over the graph.

        Yields:
            Iterator[T]: Nodes in the graph.

        Examples:
            >>> graph = MatrixGraph().from_edges([(1, 2), (3, 4)])
            >>> list(graph)
            [1, 2, 3, 4]
        """
        yield from self._nodes

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
            >>> graph = MatrixGraph().from_edges([(1, 2), (2, 3), (3, 3)])
            >>> list(graph.bfs_iterator(1))
            [1, 2, 3]
            >>> list(graph.bfs_iterator(3))
            [3]
        """
        if start not in self:
            return

        start_id = self._node_to_id[start]
        seen = Set[int]()
        queue = Queue[int].from_iterable([start_id])
        while queue:
            node = queue.dequeue()
            if node is None or node in seen:
                continue
            seen.add(node)

            yield self._nodes[node]
            for neighbor, is_neighbor in enumerate(self._matrix[node]):
                if is_neighbor:
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
            >>> graph = MatrixGraph().from_edges([(1, 2), (2, 3), (3, 3)])
            >>> list(graph.dfs_iterator(1))
            [1, 2, 3]
            >>> list(graph.dfs_iterator(3))
            [3]
        """
        if start not in self:
            return

        start_id = self._node_to_id[start]
        seen = Set[int]()
        stack = Stack[int].from_iterable([start_id])
        while stack:
            node = stack.pop()
            if node is None or node in seen:
                continue
            seen.add(node)

            yield self._nodes[node]
            for neighbor, is_neighbor in enumerate(self._matrix[node]):
                if is_neighbor:
                    stack.push(neighbor)

    def __contains__(self, value: T) -> bool:
        """Return if a given value exists in the graph.

        This checks for node containment only: the linking of edges is irrelevant to
        whether or not a node is in the graph (except that a node always exists if an
        edge from/to it exists).

        Args:
            value (T): The value to search for in the graph.

        Returns:
            bool: True if the node value is in the graph. False, otherwise.

        Examples:
            >>> graph = MatrixGraph().from_edges([(1, 2), (2, 2), (3, 4)])
            >>> 3 in graph
            True
            >>> 5 in graph
            False
        """
        return value in self._node_to_id

    def __len__(self) -> int:
        """Returns the number of nodes in the graph.

        Returns:
            int: The number of nodes in the graph.

        Examples:
            >>> graph = MatrixGraph().from_edges([(1, 2), (2, 2), (3, 4)])
            >>> len(graph)
            4
        """
        return len(self._nodes)

    def __str__(self) -> str:
        """Returns a printable display of the adjacency list graph structure.

        Returns:
            str: The printable representation of the graph.

        Examples:
            >>> graph = MatrixGraph().from_edges([(1, 2), (2, 3), (4, 4)])
            >>> print(graph)
            1 -> [2]
            2 -> [3]
            3 -> []
            4 -> [4]
        """
        out: list[str] = []
        for node_id, node in enumerate(self._nodes):
            neighbors = [
                self._nodes[i]
                for i, is_neighbor in enumerate(self._matrix[node_id])
                if is_neighbor
            ]
            out.append(f"{node} -> {neighbors}")
        return "\n".join(sort(out))

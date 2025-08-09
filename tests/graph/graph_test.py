import pytest

from dsap.graph import Graph, MatrixGraph, NodeGraph
from dsap.graph.graph import GraphBase

pytestmark = pytest.mark.parametrize(
    "cls",
    [
        Graph,
        MatrixGraph,
        NodeGraph,
    ],
)


class TestGraph:
    def test_empty_graph(self, cls: type[GraphBase[int]]) -> None:
        graph = cls()

        assert not graph
        assert len(graph) == 0
        assert str(graph) == ""
        assert list(graph) == []

    def test_from_edges(self, cls: type[GraphBase[int]]) -> None:
        graph = cls.from_edges([(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)])

        assert graph
        assert len(graph) == 5
        assert (
            str(graph)
            == """\
1 -> [2, 3]
2 -> [3, 4]
3 -> [4]
4 -> [5]
5 -> []"""
        )

        with_cycles = cls.from_edges([(1, 2), (1, 3), (2, 3), (3, 1), (3, 3), (4, 4)])
        assert len(with_cycles) == 4
        assert (
            str(with_cycles)
            == """\
1 -> [2, 3]
2 -> [3]
3 -> [1, 3]
4 -> [4]"""
        )

    def test_add(self, cls: type[GraphBase[int]]) -> None:
        graph = cls()

        graph.add(0)
        assert len(graph) == 1
        graph.add(2)
        assert len(graph) == 2
        graph.add(1)
        assert len(graph) == 3
        assert (
            str(graph)
            == """\
0 -> []
1 -> []
2 -> []"""
        )

        # Already exists in graph.
        graph.add(1)
        graph.add(1)
        assert len(graph) == 3
        assert (
            str(graph)
            == """\
0 -> []
1 -> []
2 -> []"""
        )

    def test_remove(self, cls: type[GraphBase[int]]) -> None:
        graph = cls.from_edges([(1, 2), (1, 3), (2, 3), (3, 1), (3, 3), (4, 4), (4, 5)])

        graph.remove(3)
        assert len(graph) == 4
        assert (
            str(graph)
            == """\
1 -> [2]
2 -> []
4 -> [4, 5]
5 -> []"""
        )

        graph.remove(5)
        assert len(graph) == 3
        assert (
            str(graph)
            == """\
1 -> [2]
2 -> []
4 -> [4]"""
        )

        graph.remove(4)
        assert len(graph) == 2
        assert (
            str(graph)
            == """\
1 -> [2]
2 -> []"""
        )

        graph.remove(3)
        graph.remove(0)
        graph.remove(6)
        assert len(graph) == 2

        graph.remove(1)
        graph.remove(2)
        assert not graph
        assert str(graph) == ""

    def test_add_edge(self, cls: type[GraphBase[int]]) -> None:
        graph = cls()

        graph.add_edge((0, 1))
        assert len(graph) == 2  # Both nodes are added.
        graph.add_edge((1, 0))
        assert len(graph) == 2
        graph.add_edge((1, 2))
        assert len(graph) == 3
        graph.add_edge((3, 4))
        assert len(graph) == 5
        graph.add_edge((5, 5))
        assert len(graph) == 6
        graph.add_edge((-1, 1))
        assert len(graph) == 7
        assert (
            str(graph)
            == """\
-1 -> [1]
0 -> [1]
1 -> [0, 2]
2 -> []
3 -> [4]
4 -> []
5 -> [5]"""
        )

        # Insert duplicate edges.
        graph.add_edge((0, 1))
        graph.add_edge((0, 1))
        graph.add_edge((0, 1))
        assert (
            str(graph)
            == """\
-1 -> [1]
0 -> [1]
1 -> [0, 2]
2 -> []
3 -> [4]
4 -> []
5 -> [5]"""
        )

    def test_remove_edge(self, cls: type[GraphBase[int]]) -> None:
        graph = cls.from_edges([(1, 2), (1, 3), (2, 3), (3, 1), (3, 3), (4, 4), (4, 5)])

        graph.remove_edge((1, 3))
        assert not graph.has_edge((1, 3))
        assert graph.has_edge((3, 1))
        assert len(graph) == 5

        graph.remove_edge((1, 2))
        graph.remove_edge((3, 1))
        graph.remove_edge((2, 3))
        assert len(graph) == 5  # Nodes are not actually deleted, only the links.
        assert (
            str(graph)
            == """\
1 -> []
2 -> []
3 -> [3]
4 -> [4, 5]
5 -> []"""
        )

        # Removing edges that do not exist does nothing.
        graph.remove_edge((3, 1))
        graph.remove_edge((0, 0))
        graph.remove_edge((5, 4))
        assert len(graph) == 5
        assert (
            str(graph)
            == """\
1 -> []
2 -> []
3 -> [3]
4 -> [4, 5]
5 -> []"""
        )

    def test_has_edge(self, cls: type[GraphBase[int]]) -> None:
        graph = cls.from_edges([(1, 2), (1, 3), (2, 3), (3, 1), (3, 3), (4, 4), (4, 5)])

        assert graph.has_edge((1, 2))
        assert graph.has_edge((1, 3))
        assert graph.has_edge((2, 3))
        assert graph.has_edge((3, 3))
        assert graph.has_edge((3, 1))
        assert graph.has_edge((4, 5))

        assert not graph.has_edge((5, 4))
        assert not graph.has_edge((0, 1))
        assert not graph.has_edge((1, 0))
        assert not graph.has_edge((0, 0))

    def test_contains(self, cls: type[GraphBase[int]]) -> None:
        graph = cls.from_edges([(1, 2), (1, 3), (2, 3), (3, 1), (3, 3), (4, 4), (4, 5)])

        assert 1 in graph
        assert 2 in graph
        assert 3 in graph
        assert 4 in graph
        assert 5 in graph

        assert 0 not in graph
        assert 6 not in graph

    def test_iter(self, cls: type[GraphBase[int]]) -> None:
        graph = cls.from_edges([(1, 2), (1, 3), (2, 3), (3, 1), (3, 3), (4, 4), (4, 5)])

        assert list(graph) == [1, 2, 3, 4, 5]

    def test_bfs_iterator(self, cls: type[GraphBase[int]]) -> None:
        graph = cls.from_edges([(1, 2), (1, 3), (2, 3), (3, 1), (3, 3), (4, 4), (4, 5)])

        assert list(graph.bfs_iterator(1)) == [1, 2, 3]
        assert list(graph.bfs_iterator(2)) == [2, 3, 1]
        assert list(graph.bfs_iterator(3)) == [3, 1, 2]
        assert list(graph.bfs_iterator(4)) == [4, 5]
        assert list(graph.bfs_iterator(5)) == [5]
        assert list(graph.bfs_iterator(6)) == []

    def test_dfs_iterator(self, cls: type[GraphBase[int]]) -> None:
        graph = cls.from_edges([(1, 2), (1, 3), (2, 3), (3, 1), (3, 3), (4, 4), (4, 5)])

        assert list(graph.dfs_iterator(1)) == [1, 3, 2]
        assert list(graph.dfs_iterator(2)) == [2, 3, 1]
        assert list(graph.dfs_iterator(3)) == [3, 1, 2]
        assert list(graph.dfs_iterator(4)) == [4, 5]
        assert list(graph.dfs_iterator(5)) == [5]
        assert list(graph.dfs_iterator(6)) == []

    def test_large_graph(self, cls: type[GraphBase[int]]) -> None:
        graph = cls.from_edges(
            [
                (0, 0),
                (0, 1),
                (1, 5),
                (1, 2),
                (2, 3),
                (3, 4),
                (4, 4),
                (4, 1),
                (5, 6),
                (5, 7),
                (5, 8),
                (8, 9),
                (10, 11),
                (11, 11),
                (10, 12),
                (12, 11),
                (13, 13),
            ]
        )

        assert len(graph) == 14
        assert len(list(graph.bfs_iterator(0))) == 10
        assert len(list(graph.dfs_iterator(0))) == 10
        assert len(list(graph.bfs_iterator(10))) == 3
        assert len(list(graph.dfs_iterator(10))) == 3

#!/usr/bin/env python3

import os
import sys

import unittest
import copy
import random

current_path = os.path.dirname(__file__)
src_path = os.path.abspath(os.path.join(current_path, "../src"))
sys.path.insert(0, src_path)

from adjlist import AdjacencyList
from math import inf

class TestAdjacencyList(unittest.TestCase):
    def test_is_empty(self):
        for table in [
            ([], True),
            (["a"], False),
            (["a","b"], False),
            (["b","a"], False),
        ]:
            in_sequence, want = table
            l = AdjacencyList()
            for name in in_sequence:
                l = l.add_node(name)
            self.assertEqual(l.is_empty(), want, "Added nodes {}".format(in_sequence))

    def test_add_node(self):
        for in_sequence in [
            ([]),
            (["a"]),
            (["a","b"]),
            (["b","a"]),
            (["a","b","c"]),
            (["a","c","b"]),
            (["b","a","c"]),
            (["b","c","a"]),
            (["c","a","b"]),
            (["c","b","a"]),
        ]:
            want = sorted(in_sequence)
            l = AdjacencyList()
            for name in in_sequence:
                l = l.add_node(name)
            self.assertEqual(l.list_nodes(), want, "Added nodes {}".format(in_sequence))
    
    def test_delete_node(self):
        for table in [
            ([], "a", []),
            (["a"], "a", []),
            (["a"], "b", ["a"]),
            (["a"], "B", ["a"]),
            (["a","b"], "a", ["b"]),
            (["a","b"], "b", ["a"]),
            (["a","b"], "c", ["a","b"]),
            (["a","b"], "C", ["a","b"]),
            (["a","b","c"], "a", ["b","c"]),
            (["a","b","c"], "b", ["a","c"]),
            (["a","b","c"], "c", ["a","b"]),
            (["a","b","c"], "d", ["a","b","c"]),
            (["a","b","c"], "D", ["a","b","c"]),
        ]:
            in_sequence, target, want = table
            l = AdjacencyList()
            for name in in_sequence:
                l = l.add_node(name)
            l = l.delete_node(target)
            self.assertEqual(l.list_nodes(), want, "Added nodes {}, deleted '{}'".format(in_sequence, target))

    def test_find_node(self):
        for table in [
            ([], "a", False),
            (["a"], "a", True),
            (["a"], "b", False),
            (["a"], "B", False),
            (["a","b"], "a", True),
            (["a","b"], "b", True),
            (["a","b"], "c", False),
            (["a","b"], "C", False),
            (["a","b","c"], "a", True),
            (["a","b","c"], "b", True),
            (["a","b","c"], "c", True),
            (["a","b","c"], "d", False),
            (["a","b","c"], "D", False),
        ]:
            in_sequence, target, want = table
            l = AdjacencyList()
            for name in in_sequence:
                l = l.add_node(name)
            self.assertEqual(l.find_node(target), want, "Added nodes {}, find node '{}'".format(in_sequence, target))
    
    def test_node_cardinality(self):
        for table in [
            ([], 0),
            (["a"], 1),
            (["a","b"], 2),
            (["a","b","c"], 3),
            (["a","b","c","d"], 4),
        ]:
            in_sequence, want = table
            l = AdjacencyList()
            for name in in_sequence:
                l = l.add_node(name)
            self.assertEqual(l.node_cardinality(), want, "Added nodes {}".format(in_sequence))

    def test_add_edge(self):
        for table in [
            # no nodes
            ([], [("a","a",1)], []),
            ([], [("a","b",1)], []),
            ([], [("b","a",1)], []),
            # 1 node
            (["a"], [], []),
            (["a"], [("a","a",1)], [("a","a",1)]),
            (["a"], [("a","b",1)], []),
            (["a"], [("b","a",1)], []),
            # 2 nodes
            (["a","b"], [], []),
            (["a","b"], [("a","a",1)], [("a","a",1)]),
            (["a","b"], [("a","a",1), ("a","a",1)], [("a","a",1)]),
            (["a","b"], [("a","a",1), ("a","b",1)], [("a","a",1),("a","b",1)]),
            (["a","b"], [("a","a",1), ("a","b",1),("b","a",1)], [("a","a",1),("a","b",1),("b","a",1)]),
            # 3 nodes
            (["a","b","c"], [], []),
            (["a","b","c"], [("a","a",1)], [("a","a",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1)], [("a","a",1),("a","b",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1)], [("a","a",1),("a","b",1),("a","c",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1)], [("a","a",1),("a","b",1),("a","c",1),("b","a",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1)], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1)], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1)], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1)], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)]),
        ]:
            in_nodes, in_edges, want = table
            for _ in range(10):
                random.Random(1337).shuffle(in_edges)
                l = AdjacencyList()
                for name in in_nodes:
                    l = l.add_node(name)
                for (src, dst, weight) in in_edges:
                    l = l.add_edge(src, dst, weight)
                self.assertEqual(l.list_edges(), want, "Added nodes {}, added edges {}".format(in_nodes, in_edges))
    
    def test_add_edge_update(self):
        for table in [
            # 1 node
            (["a"], [], []),
            (["a"], [("a","a",1),("a","a",2)], [("a","a",2)]),
            # 2 nodes
            (["a","b"], [("a","a",1), ("a","a",2)], [("a","a",2)]),
            (["a","b"], [("a","a",1), ("a","b",1),("b","a",1), ("a","a",2)], [("a","a",2),("a","b",1),("b","a",1)]),
            (["a","b"], [("a","a",1), ("a","b",1),("b","a",1), ("a","b",2)], [("a","a",1),("a","b",2),("b","a",1)]),
            (["a","b"], [("a","a",1), ("a","b",1),("b","a",1), ("b","a",2)], [("a","a",1),("a","b",1),("b","a",2)]),
            # 3 nodes
            (["a","b","c"], [("a","b",1),("b","b",1),("b","c",1),("a","b",2)], [("a","b",2),("b","b",1),("b","c",1)]),
            (["a","b","c"], [("a","b",1),("b","b",1),("b","c",1),("b","b",2)], [("a","b",1),("b","b",2),("b","c",1)]),
            (["a","b","c"], [("a","b",1),("b","b",1),("b","c",1),("b","c",2)], [("a","b",1),("b","b",1),("b","c",2)]),
        ]:
            in_nodes, in_edges, want = table
            l = AdjacencyList()
            for name in in_nodes:
                l = l.add_node(name)
            for (src, dst, weight) in in_edges:
                l = l.add_edge(src, dst, weight)
            self.assertEqual(l.list_edges(), want, "Added nodes {}, added edges {}".format(in_nodes, in_edges))

    def test_delete_edge(self):
        for table in [
            # empty
            ([],[],("a","a"),[]),
            # 1 node
            (["a"],[],("a","a"),[]),
            (["a"],[("a","a",1)],("a","a"),[]),
            (["a"],[("a","a",1)],("a","b"),[("a","a",1)]),
            (["a"],[("a","a",1)],("b","a"),[("a","a",1)]),
            # 2 nodes
            (["a","b"], [("a","a",1),("a","b",1),("b","a",1),("b","b",1)], ("a","a"), [("a","b",1),("b","a",1),("b","b",1)]),
            (["a","b"], [("a","a",1),("a","b",1),("b","a",1),("b","b",1)], ("a","b"), [("a","a",1),("b","a",1),("b","b",1)]),
            (["a","b"], [("a","a",1),("a","b",1),("b","a",1),("b","b",1)], ("b","a"), [("a","a",1),("a","b",1),("b","b",1)]),
            (["a","b"], [("a","a",1),("a","b",1),("b","a",1),("b","b",1)], ("b","b"), [("a","a",1),("a","b",1),("b","a",1)]),
            (["a","b"], [("a","b",1),("b","a",1),("b","b",1)], ("a","b"), [("b","a",1),("b","b",1)]),
            (["a","b"], [("b","a",1),("b","b",1)], ("b","a"), [("b","b",1)]),
            (["a","b"], [("b","b",1)], ("b","b"), []),
            # 3 nodes
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)], ("a","a"), [("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)], ("a","b"), [("a","a",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)], ("a","c"), [("a","a",1),("a","b",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)], ("b","a"), [("a","a",1),("a","b",1),("a","c",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)], ("b","b"), [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)], ("b","c"), [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("c","a",1),("c","b",1),("c","c",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)], ("c","a"), [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","b",1),("c","c",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)], ("c","b"), [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","c",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)], ("c","c"), [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1)]),

        ]:
            in_nodes, in_edges, target, want = table
            l = AdjacencyList()
            for name in in_nodes:
                l = l.add_node(name)
            for (src, dst, weight) in in_edges:
                l = l.add_edge(src, dst, weight)
            l = l.delete_edge(target[0], target[1])
            self.assertEqual(l.list_edges(), want, "Added nodes {}, added edges {}, deleted edge {}".format(in_nodes, in_edges, target))

    def test_delete_edges(self):
        for table in [
            # empty
            ([], [], "a", []),
            # 1 node
            (["a"], [], "a", []),
            (["a"], [("a","a",1)], "a", []),
            #(["a"], [("a","a",1)], "b", [("a","a",1)]),
            # 2 nodes
            (["a","b"], [("a","a",1),("a","b",1),("b","a",1),("b","b",1)], "a", [("a","b",1),("b","b",1)]),
            (["a","b"], [("a","a",1),("a","b",1),("b","a",1),("b","b",1)], "b", [("a","a",1),("b","a",1)]),
            (["a","b"], [("a","a",1),("a","b",1),("b","a",1),("b","b",1)], "c", [("a","a",1),("a","b",1),("b","a",1),("b","b",1)]),
            # 3 nodes
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)], "a", [("a","b",1),("a","c",1),("b","b",1),("b","c",1),("c","b",1),("c","c",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)], "b", [("a","a",1),("a","c",1),("b","a",1),("b","c",1),("c","a",1),("c","c",1)]),
            (["a","b","c"], [("a","a",1),("a","b",1),("a","c",1),("b","a",1),("b","b",1),("b","c",1),("c","a",1),("c","b",1),("c","c",1)], "c", [("a","a",1),("a","b",1),("b","a",1),("b","b",1),("c","a",1),("c","b",1)]),
        ]:
            in_nodes, in_edges, target, want = table
            l = AdjacencyList()
            for name in in_nodes:
                l = l.add_node(name)
            for (src, dst, weight) in in_edges:
                l = l.add_edge(src, dst, weight)
            l = l.delete_edges(target)
            self.assertEqual(l.list_edges(), want, "Added nodes {}, added edges {}, deleted edges towards node {}".format(in_nodes, in_edges, target))
    
    def test_find_edge(self):
        for table in [
            ([], [], ("a","a"), False),
            ([], [], ("a","b"), False),
            ([], [], ("b","a"), False),
            (["a"], [], ("a","a"), False),
            (["a"], [], ("a","b"), False),
            (["a"], [], ("b","a"), False),
            (["a"], [("a","a")], ("a","a"), True),
            (["a"], [("a","a")], ("a","b"), False),
            (["a"], [("a","a")], ("b","a"), False),
            (["a","b"], [], ("a","a"), False),
            (["a","b"], [], ("a","b"), False),
            (["a","b"], [], ("b","a"), False),
            (["a","b"], [("a","b"),("b","b")], ("a","a"), False),
            (["a","b"], [("a","b"),("b","b")], ("a","b"), True),
            (["a","b"], [("a","b"),("b","b")], ("b","b"), True),
            (["a","b"], [("a","b"),("b","b")], ("b","a"), False),
            (["a","b","c"], [("a","a"),("a","b"),("b","b"),("b","c"),("c","a")], ("a","a"), True),
            (["a","b","c"], [("a","a"),("a","b"),("b","b"),("b","c"),("c","a")], ("a","b"), True),
            (["a","b","c"], [("a","a"),("a","b"),("b","b"),("b","c"),("c","a")], ("a","c"), False),
            (["a","b","c"], [("a","a"),("a","b"),("b","b"),("b","c"),("c","a")], ("b","a"), False),
            (["a","b","c"], [("a","a"),("a","b"),("b","b"),("b","c"),("c","a")], ("b","b"), True),
            (["a","b","c"], [("a","a"),("a","b"),("b","b"),("b","c"),("c","a")], ("b","c"), True),
            (["a","b","c"], [("a","a"),("a","b"),("b","b"),("b","c"),("c","a")], ("c","a"), True),
            (["a","b","c"], [("a","a"),("a","b"),("b","b"),("b","c"),("c","a")], ("c","b"), False),
        ]:
            in_nodes, in_edges, target, want = table
            l = AdjacencyList()
            for name in in_nodes:
                l = l.add_node(name)
            for (src, dst) in in_edges:
                l = l.add_edge(src, dst)
            self.assertEqual(l.find_edge(target[0], target[1]), want, "Added nodes {}, added edges {}, find edge {}".format(in_nodes, in_edges, target))

    def test_edge_cardinality(self):
        for table in [
            ([], [], 0),
            (["a"], [], 0),
            (["a","b"], [], 0),
            (["a"], [("a","a")], 1),
            (["a","b"], [("a","a")], 1),
            (["a","b"], [("a","a"),("a","b")], 2),
            (["a","b"], [("a","a"),("b","a")], 2),
            (["a","b"], [("a","a"),("b","b")], 2),
            (["a","b"], [("a","a"),("a","b"),("b","a")], 3),
            (["a","b"], [("a","a"),("a","b"),("b","b")], 3),
            (["a","b"], [("a","a"),("b","a"),("b","b")], 3),
            (["a","b"], [("a","a"),("a","b"),("b","a"),("b","b")], 4),
            (["a","b","c"], [("a","b"),("b","b"),("b","c"),("c","a"),("c","c")], 5),
            (["a","b","c"], [("a","a"),("a","b"),("b","b"),("b","c"),("c","a"),("c","c")], 6),
            (["a","b","c"], [("a","a"),("a","b"),("a","c"),("b","b"),("b","c"),("c","a"),("c","c")], 7),
            (["a","b","c"], [("a","a"),("a","b"),("a","c"),("b","a"),("b","b"),("b","c"),("c","a"),("c","c")], 8),
            (["a","b","c"], [("a","a"),("a","b"),("a","c"),("b","a"),("b","b"),("b","c"),("c","a"),("c","b"),("c","c")], 9),
        ]:
            in_nodes, in_edges, want = table
            l = AdjacencyList()
            for name in in_nodes:
                l = l.add_node(name)
            for (src, dst) in in_edges:
                l = l.add_edge(src, dst)
            self.assertEqual(l.edge_cardinality(), want, "Added nodes {}, added edges {}".format(in_nodes, in_edges))

    def test_self_loops(self):
        for table in [
            ([], [], 0),
            (["a"], [], 0),
            (["a"], [("a","a")], 1),
            (["a","b"], [("a","a")], 1),
            (["a","b"], [("a","a"),("a","b"),("b","a")], 1),
            (["a","b"], [("a","a"),("a","b"),("b","a"),("b","b")], 2),
            (["a","b","c"], [("a","b"),("a","c"),("b","a"),("b","c"),("c","a"),("c","b")], 0),
            (["a","b","c"], [("a","a"),("a","b"),("a","c"),("b","a"),("b","c"),("c","a"),("c","b")], 1),
            (["a","b","c"], [("a","a"),("a","b"),("a","c"),("b","a"),("b","b"),("b","c"),("c","a"),("c","b")], 2),
            (["a","b","c"], [("a","a"),("a","b"),("a","c"),("b","a"),("b","b"),("b","c"),("c","a"),("c","b"),("c","c")], 3),
        ]:
            in_nodes, in_edges, want = table
            l = AdjacencyList()
            for name in in_nodes:
                l = l.add_node(name)
            for (src, dst) in in_edges:
                l = l.add_edge(src, dst)
            self.assertEqual(l.self_loops(), want, "Added nodes {}, added edges {}".format(in_nodes, in_edges))

    def test_adjacency_matrix(self):
        for table in [
            # no edges
            ([],[],[[]]),
            (["a"], [], [ [inf] ]),
            (["a","b"], [], [ [inf]*2, [inf]*2 ]),
            (["a","b","c"], [], [ [inf]*3, [inf]*3, [inf]*3 ]),
            # with edges (1 node)
            (["a"], [("a","a",1)], [ [1] ]),
            (["a"], [("a","a",2)], [ [2] ]),
            # with edges (2 nodes)
            (["a","b"], [("a","a",1)], [ [1,inf], [inf,inf] ]),
            (["a","b"], [("a","a",1),("a","b",2)], [ [1,2], [inf,inf] ]),
            (["a","b"], [("a","a",1),("a","b",2),("b","a",3)], [ [1,2], [3,inf] ]),
            (["a","b"], [("a","a",1),("a","b",2),("b","a",3),("b","b",4)], [ [1,2], [3,4] ]),
            (["a","b"], [("a","b",2),("b","a",3),("b","b",4)], [ [inf,2], [3,4] ]),
            (["a","b"], [("b","a",3),("b","b",4)], [ [inf,inf], [3,4] ]),
            (["a","b"], [("b","b",4)], [ [inf,inf], [inf,4] ]),
            # with edges (3 nodes)
            (["a","b","c"], [("a","a",9),("b","b",2),("c","c",13)], [ [9,inf,inf], [inf,2,inf], [inf,inf,13] ]),
            (["a","b","c"], [("a","a",9),("a","c",1),("b","b",2),("c","a",7),("c","c",13)], [ [9,inf,1], [inf,2,inf], [7,inf,13] ]),
            # with edges (4 nodes)
            (["a","b","c","d"], [("a","b",1),("b","a",4),("b","d",2),("c","c",11),("d","a",3),("d","b",1)], [ [inf,1,inf,inf], [4,inf,inf,2], [inf,inf,11,inf], [3,1,inf,inf] ]),
        ]:
            in_nodes, in_edges, want = table
            l = AdjacencyList()
            for name in in_nodes:
                l = l.add_node(name)
            for (src, dst, weight) in in_edges:
                l = l.add_edge(src, dst, weight)
            self.assertEqual(l.adjacency_matrix(), want, "Added nodes {}, added edges {}".format(in_nodes, in_edges))

if __name__ == "__main__":
    try:
        sys.exit(unittest.main())
    except KeyboardInterrupt:
        print("")
        sys.exit(1)

# Lab: tree-based data structures
This document provides a cheat-sheet on how to work with the provided
start-code.

## Use available options
```
$ ./bin/main --help
usage: Terminal-based UI - (un)directed graphs [-h] [--log-level LOG_LEVEL]
                                               [--mode MODE]

optional arguments:
  -h, --help            show this help message and exit
  --log-level LOG_LEVEL, -l LOG_LEVEL
                        Minimum verbosity for logging. Available in ascending
                        order: debug, info, warning, error, crirical.
  --mode MODE, -m MODE  Graph mode. Available options: undirected, directed.
  --echo, -e            Echo input. Useful if redirecting input from file
```

As shown above, you can specify if the program should use an (un)directed graph.
The default is directed, and you can change it by setting the undirected mode:
- Run in directed mode: `./bin/main`
- Run in undirected mode: `./bin/main -m undirected`

If you'd like to use python's logging module for debugging purposes, set the
logging level accordingly:
- Show all logging statements: `./bin/main -l debug`
- Show all but debug statements: `.bin/main -l info`
- Only show warning, error, and critical statements: `./bin/main -l warning`

## Run automated tests
To verify that your implementation works as expected, you may run the unit tests
that we use to automatically grade your lab.  Show available tests:
```
# Adjacency list
$ cat test/adjlist_test.py | grep test_ | sed 's/.*def //g' | sed 's/(self).*//g'
test_is_empty
test_add_node
test_delete_node
test_find_node
test_node_cardinality
test_add_edge
test_add_edge_update
test_delete_edge
test_delete_edges
test_find_edge
test_edge_cardinality
test_self_loops
test_adjacency_matrix

# Algorithms
$ cat test/algorithm_test.py | grep test_ | sed 's/.*def //g' | sed 's/(self).*//g'
test_dijkstra
test_prim
test_warshall
test_floyd
```

Example of running a single test:
```
$ cd test
$ python3 -m unittest -v adjlist_test.TestAdjacencyList.test_is_empty
test_is_empty (adjlist_test.TestAdjacencyList) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

Example of running an entire test suite:
```
$ python3 adjlist_test.py
.............
----------------------------------------------------------------------
Ran 13 tests in 0.014s

OK
```

If a test fails, you will get further information on why.

#!/usr/bin/env python3

import sys
import logging

log = logging.getLogger(__name__)

from math import inf

def warshall(adjlist):
    '''
    Returns an NxN matrix that contains the result of running Warshall's
    algorithm.

    Warshall's algorithm is similar to Floyd's, but gives the transitive closure
    instead of the minimum distances.

    Pre: adjlist is not empty.
    '''
    numberOfNodes = adjlist.node_cardinality()
    matrix = [[inf] * numberOfNodes for i in range(numberOfNodes)]
    matrix = floyd(adjlist)
    matrixSize = len(matrix)
    for i in range(matrixSize):
        for j in range (len(matrix[i])):
            matrix[i][j]= False if matrix[i][j] == inf else True
    return matrix


def floyd(adjlist):
    '''
    Returns an NxN matrix that contains the result of running Floyd's algorithm.

    Floyd's algorithm is similar to Warshall's, but gives the minimum distances
    instead of transitive closure.

    Pre: adjlist is not empty.
    '''
    numberOfNodes = adjlist.node_cardinality()
    index = 0
    matrix = [[inf] * numberOfNodes for i in range(numberOfNodes)]
    matrix = adjlist.create_adjacency_matrix(matrix,index,adjlist.get_head())

    for i in range(numberOfNodes):
        for j in range(numberOfNodes):
            if i == j:
                matrix [i][j] = 0
            for k in range (numberOfNodes):
                matrix[j][k] = min(matrix[j][k], (matrix[j][i] + matrix[i][k]))
    return matrix


def dijkstra(adjlist, start_node):
    '''
    Returns the result of running Dijkstra's algorithm as two N-length lists:
    1) distance d: here, d[i] contains the minimal cost to go from the node
    named `start_node` to the i:th node in the adjacency list.
    2) edges e: here, e[i] contains the node name that the i:th node's shortest
    path originated from.

    If the index i refers to the start node, set the associated values to None.

    Pre: start_node is a member of adjlist.

    === Example ===
    Suppose that we have the following adjacency matrix:

      a b c
    -+-----
    a|* 1 *
    b|* * 2
    c|* * *

    For start node "a", the expected output would then be:

    d: [ None, 1, 3]
    e: [ None, 'a', 'b' ]
    '''

    distance_list = [None] * adjlist.node_cardinality()
    edge_list = [None] * adjlist.node_cardinality()

    tmp_queue = []
    visited_nodes= []

    initialize_single_source(adjlist,tmp_queue,start_node)

    while len(tmp_queue) > 0:
        tmp_queue.sort(key=lambda node:node.get_info()[0])
        element = tmp_queue.pop(0)
        visited_nodes.append(element)

        for edge in element.get_list_of_edges():
            currNode = adjlist.get_node(edge.get_dst())
            relax(currNode,element,edge.get_weight())
        visited_nodes.sort(key = lambda node: node.get_name())

    for i, node in enumerate(visited_nodes):
        if node.get_info()[0] == 0:
            distance_list[i] = None
            edge_list[i] = None
        else:
            distance_list[i] = node.get_info()[0]
            edge_list[i] = node.get_info()[1]    

    return distance_list, edge_list

def prim(adjlist, start_node):
    '''
    Returns the result of running Prim's algorithm as two N-length lists:
    1) lowcost l: here, l[i] contains the weight of the cheapest edge to connect
    the i:th node to the minimal spanning tree that started at `start_node`.
    2) closest c: here, c[i] contains the node name that the i:th node's
    cheapest edge orignated from. 

    If the index i refers to the start node, set the associated values to None.

    Pre: adjlist is setup as an undirected graph and start_node is a member.

    === Example ===
    Suppose that we have the following adjacency matrix:

      a b c
    -+-----
    a|* 1 3
    b|1 * 1
    c|3 1 *

    For start node "a", the expected output would then be:

    l: [ None, 1, 1]
    c: [ None, 'a', 'b' ]
    '''
    weightList = [None]* adjlist.node_cardinality()
    parentList = [None]* adjlist.node_cardinality()
    queue = []

    initialize_single_source(adjlist,queue,start_node)
    
    while len(queue) != 0:
        queue.sort(key = lambda node: node.get_info()[0])
        element = queue.pop(0)

        for edge in(element.get_list_of_edges()):
            currNode = adjlist.get_node(edge.get_dst())
            if currNode in queue and edge.get_weight() < currNode.get_info()[0]:
                currNode.set_info([edge.get_weight(), element.get_name()])

    for i, node in enumerate(adjlist.get_list_of_nodes()):
        if node.get_info()[0] == 0:
            weightList[i] = None
            parentList[i] = None
        else:
            weightList[i] = node.get_info()[0]
            parentList[i] = node.get_info()[1]

    return weightList, parentList


def relax (v,u,weight):
    if v.get_info()[0] > u.get_info()[0] + weight:
        v.set_info([(u.get_info()[0] + weight), u.get_name()])


def initialize_single_source(adjlist,nodeList,Start):

    nodeList.extend(adjlist.get_list_of_nodes())

    for nodes in nodeList:
        if Start == nodes.get_name():
            nodes.set_info([0,None,None])
        else:
            nodes.set_info([inf,None,None])

if __name__ == "__main__":
    logging.critical("module contains no main")
    sys.exit(1)
 
#!/usr/bin/env python3

import sys
import logging

log = logging.getLogger(__name__)

from math import inf
from adjlist import AdjacencyList
from algorithm import dijkstra,prim,warshall,floyd

class TerminalUI:
    def __init__(self, mode="directed", echo=False):
        '''
        Selects (un)directed graph mode.
        '''
        self._mode = mode if mode=="directed" else "undirected"
        self._echo = echo
        self._adjlist = AdjacencyList()
        log.info("running in mode: {}".format(self._mode))

    def run(self):
        '''
        Provides a terminal-based UI to perform graph operations.
        '''
        self.display_menu()
        while True:
            opt, err = self.get_choice()
            if err is not None:
                self.display_error(err)
                continue
            
            if opt == "m":
                self.display_menu()
            elif opt == "v":
                self.display_graph()
            elif opt == "a":
                self.add_node()
            elif opt == "b":
                self.add_edge()
            elif opt == "d":
                self.delete_node()
            elif opt == "r":
                self.delete_edge()
            elif opt == "f":
                self.find_node()
            elif opt == "g":
                self.find_edge()
            elif opt == "D":
                self.dijkstra()
            elif opt == "F":
                self.floyd()
            elif opt == "W":
                self.warshall()
            elif opt == "P":
                self.prim()
            elif opt == "q":
                break
            else:
                log.error("menu case '{}' is missing, aborting".format(opt))
                return 1

    def menu_options(self):
        '''
        Returns a list of printable menu options.  Blank entries are interpreted
        as new lines, and single characters before the colon as hotkeys.
        '''
        return [
            "m: menu",
            "v: view",
            "q: quit",
            "",
            "a: add node",
            "b: add edge",
            "",
            "d: delete node",
            "r: delete edge",
            "",
            "f: find node",
            "g: find edge",
            "",
            "W: Warshall",
            "F: Floyd",
            "D: Dijkstra",
            "P: Prim",
        ]

    def display_menu(self):
        '''
        Shows a menu which is encapsulated between a top rule and a bottom rule.
        '''
        print(self.menu_rule("top", self.menu_width()))
        for opt in self.menu_options():
            print("\t{}".format(opt))
        print(self.menu_rule("bot", self.menu_width()))

    def menu_rule(self, pos, width):
        '''
        Returns a horizontal line using stars or tildes.
        '''
        return ("*" if pos == "top" else "~") * width

    def menu_width(self):
        '''
        Returns the menu width.
        '''
        return 32

    def menu_hotkeys(self):
        '''
        Returns a list of symbols that the menu defined as valid hotkeys.
        '''
        opts = self.menu_options()
        return [ o.split(":")[0] for o in opts if len(o.split(":")[0]) == 1 ]

    def get_choice(self):
        '''
        Attempts to read a valid menu option from the user.
        '''
        c, err = self.get_char("menu")
        if err is not None:
            return None, err
        if c not in self.menu_hotkeys():
            return None, "invalid choice"
        return c, None

    def get_node(self, msg, want):
        '''
        Attempts to read a valid node name from the user.  If `want` is False
        (True), an error is returned if the entered node is a (non-)member.
        '''
        name, err = self.get_char(msg)
        if err is not None:
            return None, err
        if want != self._adjlist.find_node(name):
            self.display_warning("node '{}' is a {}member".format(
                name, "non-" if want else ""))
        return name, None

    def get_char(self, message):
        '''
        Writes a message to stdout and waits for one-character from stdin.
        '''
        buf = input("{}> ".format(message))
        if self._echo:
            print(buf)
        if len(buf) != 1:
            return None, "invalid input (not a single character)"
        return buf, None

    def get_int(self, message):
        '''
        Writes a message to stdout and waits for an integer from stdin.
        '''
        buf = input("{}> ".format(message))
        if self._echo:
            print(buf)
        try:
            return int(buf), None
        except ValueError:
            return None, "invalid input (not an integer)"

    def get_weight(self, message, low, high):
        '''
        Writes a message to stdout and waits for an integer in [low,high].
        '''
        weight, err = self.get_int(message)
        if err is not None:
            return None, err
        if weight<low or weight>high:
            return None, "invalid input (weight must be in [{},{}])".format(low, high)
        return weight, None

    def display_graph(self):
        '''
        Displays graph info.
        '''
        if self._adjlist.is_empty():
            self.display_empty()

        nodes = self._adjlist.list_nodes()
        log.debug("all nodes: {}".format(nodes))
        log.debug("all edges: {}".format(self._adjlist.list_edges()))
        self.display_matrix_head(nodes)
        self.display_matrix_data(nodes, self._adjlist.adjacency_matrix())
        self.display_cardinality()

    def add_node(self):
        '''
        Let the user add a node to the graph.
        '''
        name, err = self.get_node("Enter node name", False)
        if err is not None:
            self.display_error(err)
            return

        self._adjlist = self._adjlist.add_node(name)

    def delete_node(self):
        '''
        Let the user delete add a node from the graph.
        '''
        name, err = self.get_node("Enter node name", True)
        if err is not None:
            self.display_error(err)
            return

        self._adjlist = self._adjlist.delete_edges(name)
        self._adjlist = self._adjlist.delete_node(name)

    def add_edge(self):
        '''
        Let the user add an edge to the graph.
        '''
        from_node, err = self.get_node("Enter from node", True)
        if err is not None:
            self.display_error(err)
            return

        to_node, err = self.get_node("Enter to node", True)
        if err is not None:
            self.display_error(err)
            return

        weight, err = self.get_weight("Enter weight", 1, 99)
        if err is not None:
            self.display_error(err)
            return

        self._adjlist = self._adjlist.add_edge(from_node, to_node, weight)
        if self._mode == "undirected":
            self._adjlist = self._adjlist.add_edge(to_node, from_node, weight)

    def delete_edge(self):
        '''
        Let the user delete an edge from the graph.
        '''
        from_node, err = self.get_node("Enter from node", True)
        if err is not None:
            self.display_error(err)
            return

        to_node, err = self.get_node("Enter to node", True)
        if err is not None:
            self.display_error(err)
            return

        if not self._adjlist.find_edge(from_node, to_node):
            self.display_error("edge ({},{}) is non-member".format(from_node, to_node))
            return

        self._adjlist = self._adjlist.delete_edge(from_node, to_node)
        if self._mode == "undirected":
            self._adjlist = self._adjlist.delete_edge(to_node, from_node)

    def find_node(self):
        '''
        Let the user search for a node in the graph.
        '''
        name, err = self.get_char("Enter node name")
        if err is not None:
            self.display_error(err)
            return

        if self._adjlist.find_node(name):
            self.display_member_node(name)
        else:
            self.display_nonmember_node(name)

    def find_edge(self):
        '''
        Let the user search for an edge in the graph.
        '''
        from_node, err = self.get_char("Enter from node")
        if err is not None:
            self.display_error(err)
            return

        to_node, err = self.get_char("Enter to node")
        if err is not None:
            self.display_error(err)
            return

        if self._adjlist.find_edge(from_node, to_node):
            self.display_member_edge(from_node, to_node)
        else:
            self.display_nonmember_edge(from_node, to_node)

    def warshall(self):
        '''
        Run Warshall's algorithm.
        '''
        if self._adjlist.is_empty():
            self.display_error("graph is empty")
            return
        
        nodes = self._adjlist.list_nodes()
        self.display_matrix_head(nodes)
        self.display_matrix_data(nodes, warshall(self._adjlist))

    def floyd(self):
        '''
        Run Floyds's algorithm.
        '''
        if self._adjlist.is_empty():
            self.display_error("graph is empty")
            return
        
        nodes = self._adjlist.list_nodes()
        self.display_matrix_head(nodes)
        self.display_matrix_data(nodes, floyd(self._adjlist))

    def dijkstra(self):
        '''
        Run Dijkstra's algorithm.
        '''
        if self._adjlist.is_empty():
            self.display_error("graph is empty")
            return
        start_node, err = self.get_node("Enter start node", True)
        if err is not None:
            self.display_error(err)
            return

        dist, prev = dijkstra(self._adjlist, start_node)
        self.display_sequence_head(self._adjlist.list_nodes())
        self.display_sequence_data([
            ("distance", dist, None),
            ("previous", prev, None),
        ])

    def prim(self):
        '''
        Run Prim's algorithm.
        '''
        if self._mode == "directed":
            self.display_error("invalid graph mode")
            return
        if self._adjlist.is_empty():
            self.display_error("graph is empty")
            return
        start_node, err = self.get_node("Enter start node", True)
        if err is not None:
            self.display_error(err)
            return

        lowcost, closest = prim(self._adjlist, start_node)
        self.display_sequence_head(self._adjlist.list_nodes())
        self.display_sequence_data([
            ("lowcost", lowcost, None),
            ("closest", closest, None),
        ])
        self.display_mst_sum(lowcost)

    def display_mst_sum(self, lowcost):
        mst_sum = sum([ v for v in lowcost if v is not None and v!=inf ])
        print("\tMST sum: {}\n".format(mst_sum))

    def display_empty(self):
        print("\n\tGraph is empty\n")

    def display_member_node(self, name):
        print("\tNode {} is a member".format(name))

    def display_nonmember_node(self, name):
        print("\tNode {} is a non-member".format(name))

    def display_member_edge(self, from_node, to_node):
        print("\tEdge ({},{}) is a member".format(from_node, to_node))

    def display_nonmember_edge(self, from_node, to_node):
        print("\tEdge ({},{}) is a non-member".format(from_node, to_node))

    def display_sequence_head(self, nodes):
        print("\n {: ^8}#".format(""), end="")
        for node in nodes:
            print(" {: ^3} ".format(node), end="")
        print("\n ========#" + "="*5*len(nodes))

    def display_sequence_data(self, data):
        for (name,sequence,star_val) in data:
            print(" {: >8}#".format(name), end="")
            for v in sequence:
                print(" {: ^3} ".format("*" if v==star_val else v), end="")
            print("")
        print("")

    def display_matrix_head(self, nodes):
        if len(nodes) == 0:
            return
        print("\n {: ^3}|".format(""), end="")
        for node in nodes:
            print(" {: ^3} ".format(node), end="")
        print("\n----+" + "-"*5*len(nodes))

    def display_matrix_data(self, nodes, matrix):
        for name,row in zip(nodes, matrix):
            print(" {: >3}|".format(name), end="")
            for col in row:
                print(" {: ^3} ".format("*" if col==inf else col), end="")
            print("")
        print("")

    def display_cardinality(self):
        node_cardinality = self._adjlist.node_cardinality()
        edge_cardinality = self._adjlist.edge_cardinality()
        if self._mode == "undirected":
            self_loops = self._adjlist.self_loops()
            edge_cardinality = int((edge_cardinality-self_loops)/2 + self_loops)
        print("node cardinality: {}".format(node_cardinality))
        print("edge cardinality: {}".format(edge_cardinality))
        print("")

    def display_error(self, err):
        print("error> {}".format(err))

    def display_warning(self, msg):
        print("warning> {}".format(msg))


if __name__ == "__main__":
    logging.critical("ui contains no main module")
    sys.exit(1)

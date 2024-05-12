from algebra.graph.node import Node

from algebra.universe import Universe
from algebra.monoid import MonoidElem


class Graph:
    nodes: set[Node]

    str2node: dict[MonoidElem, Node]
    val2node: dict[Universe, Node]


    def __init__(self):
        self.nodes = set()
        self.str2node = dict()
        self.val2node = dict()

    def add_node(self, n: Node):
        self.nodes.add(n)
        self.str2node[n.str] = n
        self.val2node[n.val] = n

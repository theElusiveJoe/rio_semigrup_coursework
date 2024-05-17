import graphviz

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

    def draw_dot(self):
        dot = graphviz.Digraph()
        for v in self.nodes:
            dot.node(v.label(), v.label())
        for v1 in self.nodes:
            for x, v2 in v1.cay_r.items():
                dot.edge(v1.label(), v2.label(), self.val2node[x].label())
        dot.render('../output/right_graph', format='png', cleanup=True) 

        dot = graphviz.Digraph()
        for v in self.nodes:
            dot.node(v.label(), v.label())
        for v1 in self.nodes:
            for x, v2 in v1.cay_l.items():
                dot.edge(v1.label(), v2.label(), self.val2node[x].label())
        dot.render('../output/left_graph', format='png', cleanup=True) 

        dot = graphviz.Digraph()
        for v in self.nodes:
            dot.node(v.label(), v.label())
        for v1 in self.nodes:
            for x, v2 in v1.cay_l.items():
                dot.edge(v1.label(), v2.label(), self.val2node[x].label())
            for x, v2 in v1.cay_r.items():
                dot.edge(v1.label(), v2.label(), self.val2node[x].label())
        dot.render('../output/lr_graph', format='png', cleanup=True) 
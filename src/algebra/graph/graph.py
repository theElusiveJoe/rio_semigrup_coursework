from enum import IntEnum
import graphviz

from algebra.universe import Universe
from algebra.monoid import MonoidElem, MonoidController

from algebra.graph.node import Node


class Lr(IntEnum):
    left = 0
    right = 1


class Graph:
    nodes: set[Node]
    S: MonoidController

    str2node: dict[MonoidElem, Node]
    val2node: dict[Universe, Node]

    def __init__(self, S: MonoidController):
        self.nodes = set()
        self.S = S
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

    def mult_nodes(self, a: Node, b: Node,
                   use_cay: bool = False, use_monoid: bool = False):
        '''
        returns Node(val = a.val * b.val)

        use_cay -- use if b is in generating nodes set

        use_monoid -- if u want to use monoid representation of b instead of directly multiply values
        '''

        match use_cay, use_monoid:
            case True, _:
                # use cay graph
                return a.cay_r[b.val]
            case _, False:
                # directly multiply
                return self.val2node[a.val * b.val]
            case _, True:
                # decompose b.str into seq of generating symbols and traverse graph
                cur = a
                monoid_string = b.str.to_symbols_seq()
                # symbols (Universe values) are generators -- so we can use cay_r
                symbols = self.S.symbols_to_values(monoid_string)
                for sym in symbols:
                    cur = a.cay_r[sym]
                return cur

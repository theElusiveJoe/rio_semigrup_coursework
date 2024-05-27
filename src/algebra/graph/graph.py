from enum import IntEnum

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
                symbols = self.S.symbols_to_values(b.str.to_symbols_seq())
                cur = a
                for sym in symbols:
                    cur = cur.cay_r[sym]
                return cur

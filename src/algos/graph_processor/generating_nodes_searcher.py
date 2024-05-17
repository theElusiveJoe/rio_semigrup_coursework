from algebra.graph import Graph
from algebra.monoid import MonoidController


def search_generating_nodes(g: Graph, mc: MonoidController):
    return [g.val2node[val] for val in mc.generators]
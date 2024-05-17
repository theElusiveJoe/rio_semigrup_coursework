from algebra.monoid import MonoidController

from algebra.graph import Graph, Node, Hclass
from algos.graph_processor import search_Hclasses, markup_idempotents, search_generating_nodes
from algos.isom_builder.models import HclassMap
from algos.isom_builder.models import MonoidMap


class IsomState:
    S1: MonoidController
    S2: MonoidController

    G1: Graph
    G2: Graph

    H1: set[Hclass]
    H2: set[Hclass]

    f: MonoidMap
    hf: HclassMap

    # all nodes from generating set of S1
    gs1_nodes: set[Node]
    # nodes from gs1_nodes, that don`t have image in f
    gs1_unmatched_nodes: set[Node]

    def __init__(self, initObjects: tuple[MonoidController,MonoidController,Graph,Graph]|None=None) -> None:
        if initObjects is None:
            return
        S1, S2, G1, G2 = initObjects
        
        if len(S1) > len(S2):
            self.S1, self.S2, self.G1, self.G2 = S2, S1, G2, G1
        else:
            self.S1, self.S2, self.G1, self.G2 = S1, S2, G1, G2

        self.gs1_nodes = set(search_generating_nodes(self.G1, self.S1))
        self.gs1_unmatched_nodes = self.gs1_nodes.copy()

        self.f = MonoidMap((self.S1, self.G1))
        self.set_f(self.G1.val2node[self.S1.identity()], self.G2.val2node[self.S2.identity()])

        markup_idempotents(self.G1)
        markup_idempotents(self.G2)

        self.H1 = set(search_Hclasses(self.G1))
        self.H2 = set(search_Hclasses(self.G2))
        self.hf = HclassMap((self.H1, self.H2))

    def set_f(self, a: Node, b: Node):
        if a in self.gs1_unmatched_nodes:
            self.gs1_unmatched_nodes.remove(a)
        self.f.map_set(a, b)

    def make_copy(self):
        newIsomState = IsomState()
        newIsomState.S1 = self.S1
        newIsomState.S2 = self.S2
        newIsomState.G1 = self.G1
        newIsomState.G2 = self.G2
        newIsomState.H1 = self.H1
        newIsomState.H2 = self.H2

        newIsomState.f = self.f.make_copy()
        newIsomState.hf = self.hf.make_copy()

        newIsomState.gs1_nodes = self.gs1_nodes
        newIsomState.gs1_unmatched_nodes = self.gs1_unmatched_nodes.copy()
        
        return newIsomState


from algebra.monoid import MonoidController
from algebra.graph import Graph
from .isom_builder_algo import IsomBuilderAlgo
from .models import IsomState

from algos.graph_builder import military_algo


def build_isomorphism(S1: MonoidController, S2: MonoidController, G1: Graph, G2: Graph) -> IsomState | None:
    return IsomBuilderAlgo(S1, S2, G1, G2).run()


def build_isomorphism_from_mc(S1: MonoidController, S2: MonoidController):
    G1 = military_algo(S1)
    G2 = military_algo(S2)
    return build_isomorphism(S1, S2, G1, G2)

def build_isomorphism_extended(S1: MonoidController, S2: MonoidController):
    G1 = military_algo(S1)
    G2 = military_algo(S2)
    algo = IsomBuilderAlgo(S1, S2, G1, G2)
    result = algo.run()
    return algo, result
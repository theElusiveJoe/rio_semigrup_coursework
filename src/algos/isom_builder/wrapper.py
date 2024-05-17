from algebra.monoid import MonoidController
from algebra.graph import Graph
from .models import IsomState
from .guesser import guess_elem

from algos.graph_builder import military_algo


def build_isomorphism(S1: MonoidController, S2: MonoidController, G1: Graph, G2: Graph):
    start_state = IsomState((S1, S2, G1, G2))
    result, _ = guess_elem(start_state)
    return result


def build_isomorphism_from_mc(S1: MonoidController, S2: MonoidController):
    G1 = military_algo(S1)
    G2 = military_algo(S2)
    return build_isomorphism(S1, S2, G1, G2)

from algos.isom_builder.models import IsomState
from algos.graph_builder import military_algo
from algebra.monoid import MonoidController


def check(state: IsomState) -> bool:
    gs1 = state.gs1_nodes
    # it is strange, if we call check, but generating node doesn`t have image`
    # so the state.f can be unsafe here
    gs2 = list(state.f[x].val for x in gs1)

    image_mc = MonoidController(gs2)
    image_graph = military_algo(image_mc)

    return len(state.G1.nodes) == len(image_graph.nodes)

import random

from algebra.graph import Graph
from algebra.monoid import MonoidController
from algebra.utils.monoid_power import naive_monoid_power
from algos.graph_builder import military_algo
import samples

random.seed(42)


def check_graph(g: Graph, S: MonoidController):
    assert len(g.nodes) == naive_monoid_power(S)

    for node in g.nodes:
        for vai in S.generators:
            assert vai * node.val == node.cay_l[vai].val
            assert node.val * vai == node.cay_r[vai].val

    return True


def test_simple_samples():
    for S in samples.SIMPLE_SAMPLES_LIST:
        graph = military_algo(S)
        assert check_graph(graph, S)


def test_random_samples():
    for _ in range(50):
        S = samples.gen_random_sample(
            set_size=random.randint(2, 4),
            generators_num=random.randint(1, 5)
        )
        graph = military_algo(S)
        assert check_graph(graph, S)

import itertools
import random

from algebra.graph import Graph
from algebra.monoid import MonoidController
from algebra.universe.abstract import Universe
from algos.graph_builder import military_algo
from algos.graph_processor import search_H_classes
import samples


def check_h_classes(g: Graph):
    hclasses = search_H_classes(g)
    all_values = set(map(lambda x: x.val, g.nodes))

    def get_elem_l_and_r_class(x: Universe):
        lclass = set(map(lambda val: val*x, all_values))
        rclass = set(map(lambda val: val*x, all_values))
        return lclass, rclass

    for hclass in hclasses:
        elems = hclass.elems
        target_elem = elems.pop()
        target_classes = get_elem_l_and_r_class(target_elem.val)
        for elem in elems:
            assert target_classes == get_elem_l_and_r_class(elem.val)

    return True


def test_simple_samples():
    for S in samples.SIMPLE_SAMPLES_LIST:
        graph = military_algo(S)
        assert check_h_classes(graph)


def test_random_samples():
    for _ in range(100):
        S = samples.gen_random_sample(
            set_size=random.randint(2, 5),
            generators_num=random.randint(1, 5)
        )
        graph = military_algo(S)
        assert check_h_classes(graph)

import random
import samples

from algos.graph_processor import search_Hclasses
from algos.graph_builder import military_algo
from algebra.universe.abstract import Universe
from algebra.graph import Graph

random.seed(42)


def check_hclasses(g: Graph):
    all_values = set(map(lambda x: x.val, g.nodes))

    def get_h_class_by_def(n: Universe):
        return set(map(lambda x: x*n, all_values)).intersection(set(map(lambda x: n*x, all_values)))

    hclasses = search_Hclasses(g)
    hclasses_values = set(map(
        lambda hclass: frozenset(map(lambda elem: elem.val, hclass.elems)),
        hclasses))

    assert len(hclasses_values) == len(hclasses)

    for a in hclasses_values:
        for b in hclasses_values:
            if a == b:
                continue
            assert len(a.intersection(b)) == 0

    for hclass in hclasses:
        assert hclass.size > 0
        elems = hclass.elems
        target_elem = list(elems)[0]
        target_classes = get_h_class_by_def(target_elem.val)
        for elem in elems:
            assert target_classes == get_h_class_by_def(elem.val)

    return True


def test_simple_samples():
    for S in samples.SIMPLE_SAMPLES_LIST:
        graph = military_algo(S)
        assert check_hclasses(graph)


def test_random_samples():
    for _ in range(50):
        S = samples.gen_random_sample(
            set_size=random.randint(2, 5),
            generators_num=random.randint(1, 4)
        )
        graph = military_algo(S)
        assert check_hclasses(graph)


def test_hclasses_stability():
    '''
    как бы граф не был оформлен, множесто H-классов должно совпадать
    '''
    for _ in range(50):
        S = samples.gen_random_sample(
            set_size=random.randint(2, 4),
            generators_num=random.randint(1, 5)
        )

        S1, S2 = S.mixed(), S.mixed()
        G1, G2 = military_algo(S1), military_algo(S2)
        H1, H2 = search_Hclasses(G1), search_Hclasses(G2)

        assert len(H1) == len(H2)

        unmatched_classes = H2
        for h1 in H1:
            h2_res = None
            for h2 in unmatched_classes:
                if h1.size != h2.size:
                    continue
                h1_values = set(map(lambda x: x.val, h1.elems))
                h2_values = set(map(lambda x: x.val, h2.elems))
                if h1_values != h2_values:
                    continue
                h2_res = h2
                break

            assert h2_res is not None
            unmatched_classes.remove(h2_res)

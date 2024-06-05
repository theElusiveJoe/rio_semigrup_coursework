from functools import reduce

from algebra.monoid.controller import MonoidController
from algebra.universe.abstract import Universe
from algos.graph_builder import military_algo

from algos.isom_builder.shared.algo_init_set import AlgoInitSet

from algos.isom_builder.eco.isom_state import IsomState
from algos.isom_builder.naive.simple_isom import SimpleIsom


def check_isom(init_set: AlgoInitSet, isom: IsomState | SimpleIsom) -> bool:
    '''
    строим моноид из образов generating_set_1
    проверяем, что рамеры графов совпадают
    '''
    if type(isom) == IsomState:
        gs2 = list(map(lambda x: x.val, isom.f.gen_set_map.values()))
    elif type(isom) == dict:
        gs2 = list(map(lambda x: x.val, isom.values()))
    else:
        raise RuntimeError(f'unknown isom type:{type(isom)}')

    image_mc = MonoidController(gs2)
    image_graph = military_algo(image_mc)
    if len(init_set.G1.nodes) != len(image_graph.nodes):
        return False

    total_map: dict[Universe, Universe] = dict()
    for a in init_set.G1.nodes:
        for b in init_set.G1.nodes:
            ab_val = a.val * b.val
            # найдем разложение a на элементы generating_set_1
            a_decomp = [init_set.G1.val2node[x]
                        for x in init_set.S1.symbols_to_values(a.str.to_symbols_seq())]
            # найдем разложение b на элементы generating_set_1
            b_decomp = [init_set.G1.val2node[x]
                        for x in init_set.S1.symbols_to_values(b.str.to_symbols_seq())]
            # разложение ab
            ab_decomp = a_decomp + b_decomp

            if ab_decomp == [] and ab_val.is_identity():
                continue

            # список образов разложения ab
            if type(isom) == IsomState:
                ab_decomp_image = [isom.f.all_map[x] for x in ab_decomp]
            elif type(isom) == dict:
                ab_decomp_image = [isom[x] for x in ab_decomp]
            else:
                raise RuntimeError(f'unknown isom type: {isom}:{type(isom)}')

            # перемножим
            ab_val_image = reduce(
                lambda x, y: x * y.val, ab_decomp_image[1:], ab_decomp_image[0].val)

            ab_val_exists_image = total_map.get(ab_val)
            if ab_val_exists_image is None:
                total_map[ab_val] = ab_val_image
            else:
                if ab_val_exists_image != ab_val_image:
                    return False

    return True

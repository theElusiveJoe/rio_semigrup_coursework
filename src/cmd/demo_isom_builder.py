import random
# random.seed(44)
from algebra.utils import prepare_generating_set
import samples
from samples import simple_samples
from algos.isom_builder import build_isomorphism_from_mc

from functools import reduce
import random
random.seed(42)

from algebra.monoid import MonoidController

from algebra.universe.abstract import Universe
from algos.isom_builder import build_isomorphism_extended
from algos.isom_builder.models import IsomState
from algos.isom_builder.isom_builder_algo import IsomBuilderAlgo

import samples



def isom_deep_check(algo: IsomBuilderAlgo, result: IsomState):
    total_map: dict[Universe, Universe] = dict()
    print('GO DEEP CHECK')
    for a in algo.G1.nodes:
        for b in algo.G1.nodes:
            ab_val = a.val * b.val
            # найдем разложение a на элементы generating_set_1
            a_decomp = [algo.G1.val2node[x]
                        for x in algo.S1.symbols_to_values(a.str.to_symbols_seq())]
            # найдем разложение b на элементы generating_set_1
            b_decomp = [algo.G1.val2node[x]
                        for x in algo.S1.symbols_to_values(b.str.to_symbols_seq())]
            # разложение ab
            ab_decomp = a_decomp + b_decomp
            
            if ab_decomp == [] and ab_val.is_identity():
                continue

            # список образов разложения ab
            ab_decomp_image = [result.f.all_map[x] for x in ab_decomp]
            # перемножим
            ab_val_image = reduce(lambda x,y: x * y.val, ab_decomp_image[1:], ab_decomp_image[0].val)

            ab_val_exists_image = total_map.get(ab_val)
            if ab_val_exists_image is None:
                total_map[ab_val] = ab_val_image
            else:
                if ab_val_exists_image != ab_val_image: 
                    print(a,b)
                    print(ab_val_exists_image)
                    print(ab_val_image)
                    assert False


def check_isomorphism_build(S: MonoidController):
    S1, S2 = S.mixed(), S.mixed()
    algo, isom = build_isomorphism_extended(S1, S2)
    assert isom is not None
    # isom_deep_check(algo, isom)


def main():
    # S1 = prepare_generating_set(simple_samples.T3_SPIN_PLUS.generators)
    # S2 = simple_samples.T3_SPIN_PLUS
    # res = build_isomorphism_from_mc(S1, S2.mixed())
    # # print(res)

    # S = samples.gen_random_sample(
    #     set_size=random.randint(2, 5),
    #     generators_num=random.randint(1, 5)
    # )
    # print(S.generators)
    
    # S = samples.funny_samples.FUNNY_LOOP_WITH_CENTER
    # S1, S2 = S.mixed(), S.mixed()
    # res = build_isomorphism_from_mc(S1, S2)
    # print(res)

    for _ in range(1000):
        S = samples.gen_random_sample(
            set_size=random.randint(2, 5),
            generators_num=random.randint(1, 3)
        )
        print(S.generators)
        check_isomorphism_build(S)



main()

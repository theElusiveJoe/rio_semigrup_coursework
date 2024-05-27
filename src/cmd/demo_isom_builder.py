import random

from algebra.utils import prepare_generating_set
from algos.isom_builder import build_isomorphism_from_mc
from samples import simple_samples
import samples

random.seed(42)


def main():
    print('generators:')
    print(simple_samples.T3_SPIN_PLUS.generators)
    print()

    print('without prepare generating set:')
    S1 = simple_samples.T3_SPIN_PLUS
    S2 = simple_samples.T3_SPIN_PLUS
    res = build_isomorphism_from_mc(S1, S2.mixed())
    print(res.f)  # type: ignore
    print()

    print('with prepare generating set:')
    print('unnecessary elems removed')
    S1 = prepare_generating_set(simple_samples.T3_SPIN_PLUS.generators)
    S2 = simple_samples.T3_SPIN_PLUS
    res = build_isomorphism_from_mc(S1, S2.mixed())
    print(res.f)  # type: ignore
    print()

    print('------------------------------------------')
    S = samples.funny_samples.FUNNY_LOOP_WITH_CENTER
    print('generators:')
    print(S.generators)
    print('ожидайте, это на долго')
    S1, S2 = S.mixed(), S.mixed()
    res = build_isomorphism_from_mc(S1, S2)
    print(res.f)  # type: ignore


main()

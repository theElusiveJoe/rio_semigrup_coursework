import random

from algebra.monoid import MonoidController
from algos.isom_builder.wrapper import build_isomorphism_from_mc
import samples

random.seed(42)


def check_isomorphism_build(S: MonoidController):
    S1, S2 = S.mixed(), S.mixed()
    isom = build_isomorphism_from_mc(S1, S2)
    assert isom is not None


def test_simple_samples():
    for S in samples.SIMPLE_SAMPLES_LIST:
        check_isomorphism_build(S)


def test_random_samples():
    for _ in range(50):
        S = samples.gen_random_sample(
            set_size=random.randint(2, 4),
            generators_num=random.randint(1, 5)
        )
        check_isomorphism_build(S)

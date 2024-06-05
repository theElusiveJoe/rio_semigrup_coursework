import random

from algebra.monoid import MonoidController
from algos.isom_builder.shared.algo_config import get_all_configs
from algos.isom_builder.wrapper import eco_isom  
import samples

random.seed(42)


def check_isomorphism_build(S: MonoidController):
    S1, S2 = S.mixed(), S.mixed()
    for config in get_all_configs():
        isom = eco_isom(S1, S2, config)
        assert isom is not None


def test_simple_samples():
    for S in samples.SIMPLE_SAMPLES_LIST:
        check_isomorphism_build(S)


def test_random_samples():
    for _ in range(10):
        S = samples.gen_random_sample(
            set_size=random.randint(2, 2),
            generators_num=random.randint(1, 5)
        )
        check_isomorphism_build(S)

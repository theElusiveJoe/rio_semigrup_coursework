import random

from algebra.monoid import MonoidController
from algos.graph_builder import military_algo
from algos.isom_builder.shared.algo_config import AlgoConfig, get_all_configs
from algos.isom_builder.wrapper import eco_isom  
import samples

random.seed(42)


def check_isomorphism_build(S: MonoidController):
    S1, S2 = S.mixed(), S.mixed()
    for config in [AlgoConfig()]:
        isom = eco_isom(S1, S2, config)
        assert isom is not None


def test_simple_samples():
    for S in samples.SIMPLE_SAMPLES_LIST:
        check_isomorphism_build(S)


def test_random_samples():
    for _ in range(100):
        while True:
            S = samples.gen_random_sample(
            set_size=random.randint(5,5),
            generators_num=random.randint(1, 4)
            )
            if len(military_algo(S).nodes) < 100:
                break

        check_isomorphism_build(S)

test_random_samples()
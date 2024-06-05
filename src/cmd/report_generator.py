import time
from typing import Any
from algebra.monoid.controller import MonoidController
from algos.isom_builder.models.algo_config import AlgoConfig
from algos.isom_builder.wrapper import build_isomorphism_from_mc
from samples import funny_samples, simple_samples
from utils.tester.timer import timer


def time_measurement(tests: dict[Any, MonoidController], config: AlgoConfig):
    results = dict()
    for name, S in tests.items():
        S1, S2 = S, S
        t, _ = timer(lambda: build_isomorphism_from_mc(S1, S2, config))

        results[name] = t

    return results


tests = {
    't3spin': funny_samples.FUNNY_LOOP_WITH_CENTER
}


def main():
    config = AlgoConfig()
    time_stats = time_measurement(tests, config)
    print(time_stats)


if __name__ == '__main__':
    main()

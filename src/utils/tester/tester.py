from dataclasses import dataclass
from pprint import pp
from typing import Callable, Generic, NamedTuple, TypeVar

from tqdm import tqdm

from algebra.monoid.controller import MonoidController
from algos.isom_builder.shared.algo_config import AlgoConfig
from utils.events.eventsHandler import EH


inputType = TypeVar('inputType')
intermediateType = TypeVar('intermediateType')
resultType = TypeVar('resultType')

inStats = TypeVar('inStats')
postStats = TypeVar('postStats')
comboStats = TypeVar('comboStats')
sumStats = TypeVar('sumStats')


@dataclass
class FuncSet(Generic[inputType, intermediateType,
              resultType, inStats, postStats, comboStats, sumStats]):
    preparator: Callable[[inputType], intermediateType]
    f: Callable[[intermediateType], resultType]
    inProcessor: Callable[[Callable[[intermediateType], resultType], intermediateType],
                          tuple[inStats, resultType]]
    postProcessor: Callable[[], postStats]
    statsComposer: Callable[[tuple[inStats, postStats]], comboStats]
    sumUpper: Callable[[list[comboStats]], sumStats]


class TestCase(NamedTuple):
    name: str
    S: MonoidController


class NamedConfig(NamedTuple):
    name: str
    config: AlgoConfig


def run_single_time(
    fs: FuncSet[inputType, intermediateType, resultType, inStats, postStats, comboStats, sumStats],
    args: inputType,
) -> comboStats:
    tmp = fs.preparator(args)
    EH.reset()
    inStats, _ = fs.inProcessor(fs.f, tmp)
    postStats = fs.postProcessor()
    EH.reset()
    comboStats = fs.statsComposer((inStats, postStats))
    return comboStats


def run_single_tests_family(
    fs: FuncSet[inputType, intermediateType, resultType, inStats, postStats, comboStats, sumStats],
    args_list: list[inputType],
) -> sumStats:
    results = []
    for args in args_list:
        results.append(run_single_time(fs, args))

    return fs.sumUpper(results)


def run_one_semigroup(S: MonoidController, n: int,
                      configs: list[NamedConfig], fs: FuncSet):
    results = dict()
    S_variations = list(set([(S.mixed(), S.mixed()) for _ in range(n)]))

    for conf in configs:
        print(f'config: {conf.name}')
        test_family = [(x[0], x[1], conf.config) for x in S_variations]
        results[conf.name] = run_single_tests_family(fs, test_family)
    # pp(results)
    return results


def run_tests(tests_list: list[TestCase],
              configs: list[NamedConfig], fs: FuncSet, variations_num: int):
    results = dict()
    for tc in tests_list:
        print(f"test case: {tc.name}")
        results[tc.name] = run_one_semigroup(tc.S, variations_num, configs, fs)
    return results

from typing import TypeAlias

from algebra.monoid import MonoidController
from algebra.graph import Graph, Node

from algos.isom_builder.naive.simple_isom import SimpleIsom
from algos.isom_builder.shared.algo_config import AlgoConfig
from algos.isom_builder.shared.algo_init_set import AlgoInitSet
from algos.isom_builder.shared.check import check_isom

from utils.events import spawn_event, Event, event_on_startup


class IsomBuilderNaiveAlgo:
    S1: MonoidController
    S2: MonoidController

    G1: Graph
    G2: Graph

    init_set: AlgoInitSet

    s1_generators: list[Node]

    def __init__(self, init_set: AlgoInitSet):
        self.S1, self.S2, self.G1, self.G2 = init_set.S1, init_set.S2, init_set.G1, init_set.G2
        self.config = init_set.config if init_set.config is not None else AlgoConfig()
        self.init_set = init_set

        self.s1_generators = [self.G1.val2node[val]
                              for val in self.S1.generators]

    def run(self) -> SimpleIsom | None:
        return self.guess(SimpleIsom(), set(), 0)

    def guess(self, isom: SimpleIsom,
              images: set[Node], i: int) -> SimpleIsom | None:
        if i == len(self.S1.generators):
            return self.check(isom)

        a = self.s1_generators[i]
        for b in filter(
                lambda x: x not in images and not x.is_identity(), self.G2.nodes):
            res = self.guess(
                isom | {a: b}, images | {b}, i + 1
            )
            if res:
                return res

        return None

    def check(self, isom: dict[Node, Node]) -> SimpleIsom | None:
        if check_isom(self.init_set, isom):
            return isom
        return None

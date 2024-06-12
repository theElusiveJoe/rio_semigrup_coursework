
from dataclasses import dataclass, field

from algebra.graph.graph import Graph
from algebra.graph.hclass import Hclass
from algebra.monoid.controller import MonoidController

from .algo_config import AlgoConfig


@dataclass
class AlgoInitSet:
    S1: MonoidController
    S2: MonoidController
    G1: Graph
    G2: Graph
    H1: set[Hclass]
    H2: set[Hclass]
    config: AlgoConfig = field(default_factory=lambda: AlgoConfig())

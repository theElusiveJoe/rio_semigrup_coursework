from algebra.monoid import MonoidController
from algebra.graph import Graph
from algos.graph_processor.hclasses_searcher import search_Hclasses
from algos.graph_processor.idempotents_markupper import markup_idempotents

from algos.graph_builder import military_algo
from algos.isom_builder.shared.algo_config import AlgoConfig
from algos.isom_builder.shared.algo_init_set import AlgoInitSet

from algos.isom_builder.eco.eco_algo import IsomBuilderEcoAlgo
from algos.isom_builder.naive.naive_algo import IsomBuilderNaiveAlgo


def create_init_set(S1: MonoidController, S2: MonoidController, config: AlgoConfig | None = None):
    G1 = military_algo(S1)
    G2 = military_algo(S2)
    markup_idempotents(G1)
    markup_idempotents(G2)
    H1 = set(search_Hclasses(G1))
    H2 = set(search_Hclasses(G2))
    init_set = AlgoInitSet(S1=S1, S2=S2, G1=G1, G2=G2, H1=H1, H2=H2,
                           config=config if config else AlgoConfig())
    return init_set


def eco_isom_extended(
        S1: MonoidController, S2: MonoidController, config: AlgoConfig | None = None):
    init_set = create_init_set(S1, S2, config)
    algo = IsomBuilderEcoAlgo(init_set)
    result = algo.run()
    return algo, result


def eco_isom(
        S1: MonoidController, S2: MonoidController, config: AlgoConfig | None = None):
    _, res = eco_isom_extended(S1, S2, config)
    return res


def naive_isom(
        S1: MonoidController, S2: MonoidController, config: AlgoConfig | None = None):
    init_set = create_init_set(S1, S2, config)
    algo = IsomBuilderNaiveAlgo(init_set)
    res = algo.run()
    return res

from algebra import graph
from samples import simple_samples

from algos.graph_builder import military_algo
from algos.graph_processor import markup_idempotents, search_Hclasses


def main():
    S = simple_samples.T3_SPIN
    graph = military_algo(S)
    graph.draw_dot()


main()

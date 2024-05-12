from algebra import graph
from samples import simple_samples

from algos.graph_builder import military_algo


def main():
    S = simple_samples.T6_PAPER_SAMPLE
    graph = military_algo(S)


main()

from samples import simple_samples

from algos.graph_builder import military_algo
from utils.painter.graph_painter import paint_graph


def main():
    S = simple_samples.T6_PAPER_SAMPLE
    graph = military_algo(S)
    filename = paint_graph(graph, filename="demo_T6_PAPER_EXAMPLE")
    print(f'check {filename} for graph')


main()

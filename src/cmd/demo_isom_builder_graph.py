import random

from algebra.utils import prepare_generating_set
from algos.isom_builder.wrapper import eco_isom_extended
from utils.painter.graph_painter import paint_graph
import samples

random.seed(42)


def main():
    S = samples.simple_samples.T3_SPIN_PLUS
    print('generators:')
    print(S.generators)
    print()

    print('wait a bit')
    algo, isom = eco_isom_extended(
        S, prepare_generating_set(S.mixed().generators))
    assert isom is not None  # чтобы тайпчекер не ругался
    print('drawing a braph...')
    filename = paint_graph(
        algo.G1,
        algo.G2,
        isom.hf.H1,
        isom.hf.H2,
        isom.f,
        'demo_T3_SPIN_PLUS')
    print(f'check {filename} for graph')


main()

from samples import simple_samples

from algos.graph_builder import military_algo
from algos.graph_processor import markup_idempotents, search_Hclasses


def main():
    S = simple_samples.T4_ENTIRE
    print('полугруппа T4:')
    print(S.generators)
    graph = military_algo(S)
    markup_idempotents(graph)
    hclasses = search_Hclasses(graph)
    print('H-классы')
    for hclass in hclasses:
        print(hclass)


main()

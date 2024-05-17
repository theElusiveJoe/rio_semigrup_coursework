from algebra import graph
from samples import simple_samples
from algos.isom_builder import build_isomorphism_from_mc


def main():
    S1 = simple_samples.T3_SPIN
    S2 = simple_samples.T3_SPIN

    res = build_isomorphism_from_mc(S1, S2)
    print(res)

main()

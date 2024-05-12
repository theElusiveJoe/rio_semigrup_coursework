from typing import Any, Sequence
from algebra.monoid import MonoidController
from algebra.universe.abstract import Universe
from algebra.utils.monoid_power import naive_monoid_power


def filter_identity(generators: Sequence[Universe]):
    return list(filter(lambda x: not x.is_identity(), generators))

def minimize_generating_set(generators: list[Universe]):
    gen_set = set(generators)
    n_target = naive_monoid_power(MonoidController(generators))

    for elem in generators:
        new_gen_set = gen_set.difference({elem})
        if len(new_gen_set) == 0:
            break

        n_new = naive_monoid_power(MonoidController(list(new_gen_set)))

        if n_new == n_target:
            gen_set = new_gen_set

    return list(gen_set)


def prepare_generating_set(generators: Sequence[Universe], minimize=True):
    generators = filter_identity(generators)
    if minimize:
        generators = minimize_generating_set(generators)
    return MonoidController(generators)


def prepare_generating_set_from_description(universe_type: type[Universe], *description: Any, minimize=True):
    generators = list(map(universe_type, description))
    return prepare_generating_set(generators, minimize)

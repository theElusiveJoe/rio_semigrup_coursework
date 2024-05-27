import itertools
from algebra.monoid.controller import MonoidController
from algebra.universe.abstract import Universe


def naive_monoid_power(S: MonoidController):
    checked_values: set[Universe] = set()
    unchecked_values = {S.identity()}
    generators = S.generators

    while True:
        new_values = {pair[0] * pair[1]
                      for pair in itertools.product(list(unchecked_values), list(generators))}
        new_values.difference_update(checked_values)
        new_values.difference_update(unchecked_values)
        if len(new_values) == 0:
            return len(checked_values | unchecked_values)

        checked_values |= unchecked_values
        unchecked_values = new_values

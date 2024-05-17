from typing import Iterable
from more_itertools import first

from algebra.graph.node import Node


class Hclass:
    elems: frozenset[Node]
    size: int
    has_idempotent: bool
    has_e: bool
    idempotent: None | Node

    def __init__(self, elems: Iterable[Node]):
        self.elems = frozenset(elems)
        self.size = len(self.elems)

        self.idempotent = first(
            filter(lambda x: x.is_idempotent, self.elems), None)
        if self.idempotent is None:
            self.has_idempotent = False
            self.has_e = False
        else:
            self.has_idempotent = True
            self.has_e = self.idempotent.is_identity()

        for node in self.elems:
            node.hclass = self

    def __repr__(self):
        return f'H{{{" ".join(map(str, self.elems))}}}'

    def __hash__(self):
        return hash(self.elems)

    def assign_to_elems(self):
        for x in self.elems:
            x.assign_hclass(self)

from __future__ import annotations

from typing import Iterable
from more_itertools import first

from algebra.graph.node import Node


class Hclass:
    elems: frozenset[Node]
    size: int
    idempotent: None | Node

    def __init__(self, elems: Iterable[Node]):
        self.elems = frozenset(elems)
        self.size = len(self.elems)

        self.idempotent = first(
            filter(lambda x: x.is_idempotent, self.elems), None)

        for node in self.elems:
            node.assign_hclass(self)

    def has_idempotent(self):
        return self.idempotent is not None

    def has_e(self):
        return self.idempotent is not None and self.idempotent.val.is_identity()

    def __repr__(self):
        return f'H{{{" ".join(map(str, self.elems))}}}'

    def __hash__(self):
        return hash(self.elems)

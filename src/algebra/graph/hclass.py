from typing import Iterable

from more_itertools import first
from algebra.graph import Node


class Hclass:
    elems: set[Node]
    size: int
    has_idempotent: bool
    has_e: bool
    idempotent: None|Node

    def __init__(self, elems: Iterable[Node]):
        self.elems = set(elems)
        self.size = len(self.elems)

        self.idempotent = first(filter(lambda x: x.is_idempotent, self.elems), None)
        if self.idempotent is None:
            self.has_idempotent = False
            self.has_e = False
        else:
            self.has_idempotent = True
            self.has_e = self.idempotent.is_identity()

    def __repr__(self):
        return f'H{{{" ".join(map(str, self.elems))}}}'



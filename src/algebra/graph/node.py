from __future__ import annotations
import typing

from algebra.universe import Universe
from algebra.monoid import MonoidElem

# need to avoid cercular import
if typing.TYPE_CHECKING:
    from .hclass import Hclass


class Node:
    val: Universe
    str: MonoidElem

    cay_l: dict[Universe, Node]
    cay_r: dict[Universe, Node]

    _hclass: Hclass

    is_idempotent: bool

    flag1: bool

    def __init__(self, val: Universe, str: MonoidElem):
        self.val = val
        self.str = str

        self.cay_l, self.cay_r = dict(), dict()

        self.is_idempotent = False

        self.flag1 = False
        self._hclass = None  # type: ignore

    def __hash__(self):
        return hash(self.str)

    def __repr__(self) -> str:
        return f'Node({self.str})'

    def set_cay_l(self, x: Universe, n: Node):
        self.cay_l[x] = n

    def set_cay_r(self, x: Universe, n: Node):
        self.cay_r[x] = n

    def is_identity(self):
        return self.str.is_identity()

    def label(self):
        return str(self.str)

    def get_hclass(self) -> Hclass:
        return self._hclass

    def assign_hclass(self, hclass: Hclass):
        # to ensure, we don`t assign hclass twice
        assert self._hclass is None
        self._hclass = hclass

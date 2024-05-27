from __future__ import annotations
from enum import Enum

from algebra.graph import Graph, Node


class ChainMultipleType(Enum):
    generator = 1
    monoid_multiply = 2
    graph_traverse = 3


class Chain:
    '''
    цепь может быть:
        * завершенной --- т.е. в ней нашелся цикл
        * не завершенной --- она находится в процессе построения

    последний элемент цепи хранится --- он дублируется
    '''

    elems: list[Node]
    is_completed: bool
    repeat_degree: int
    multiple_type: ChainMultipleType
    graph: Graph

    def __init__(self, base: Node, multiple_type: ChainMultipleType,
                 graph: Graph) -> None:
        self.is_completed = False
        self.repeat_degree = -1
        self.elems = [base]
        self.multiple_type = multiple_type
        self.graph = graph

    def __str__(self) -> str:
        return '->'.join(map(str, self.elems))

    def len(self):
        return len(self.elems)

    def base(self):
        return self.elems[0]

    def last(self):
        return self.elems[-1]

    def build_next(self) -> Node:
        new_degree: Node
        match self.multiple_type:
            case ChainMultipleType.generator:
                new_degree = self.graph.mult_nodes(
                    self.last(), self.base(), use_cay=True)
            case ChainMultipleType.monoid_multiply:
                new_degree = self.graph.mult_nodes(
                    self.last(), self.base(), use_cay=False, use_monoid=True)
            case ChainMultipleType.graph_traverse:
                new_degree = self.graph.mult_nodes(
                    self.last(), self.base(), use_cay=False, use_monoid=False)

        try:
            idx = self.elems.index(new_degree)
            self.repeat_degree = idx + 1
            self.is_completed = True
        except ValueError:
            pass

        self.elems.append(new_degree)
        return new_degree

    def get_degree(self, d: int):
        return self.elems[d - 1]

    def has_degree(self, d: int):
        return self.len() >= d

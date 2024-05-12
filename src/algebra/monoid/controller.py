from __future__ import annotations

from typing import Any
from algebra.universe.abstract import Universe
from .element import MonoidElem


class IdentityInGeneratorsException(Exception):
    pass

class EmptyGeneratorsSetException(Exception):
    pass


class MonoidController:
    universe_type: type[Universe]
    generators: list[Universe]

    def __init__(self, seq: list[Universe]) -> None:
        if len(seq) == 0:
            raise EmptyGeneratorsSetException("generators set is empty")
        
        self.universe_type = type(seq[0])

        if seq[0].identity() in seq:
            raise IdentityInGeneratorsException(f'identity elem can not be generator')

        self.generators = seq

    def __len__(self):
        return len(self.generators)

    def __getitem__(self, key: int):
        return self.generators[key]

    def identity(self) -> Universe:
        return self.generators[0].identity()

    def get_value_i(self, i: int):
        return self.generators[i]

    def get_string_i(self, i: int):
        return MonoidElem.from_char(i)

    # @staticmethod
    # def build_from_description(universe_type: type[Universe], *descriptions: Any) -> MonoidController:
    #     generators = list(map(universe_type, descriptions))
    #     return MonoidController(generators)

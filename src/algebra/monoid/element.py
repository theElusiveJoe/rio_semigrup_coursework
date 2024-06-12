from __future__ import annotations


base = 1000


def encode(seq: list[int]) -> int:
    res = 0
    for x in seq:
        res *= base
        res += (x + 1)
    return res


def decode(t: int | MonoidElem) -> list[int]:
    s = 0
    if isinstance(t, MonoidElem):
        s = t.symbols
    elif isinstance(t, int):
        s = t

    res = []
    while s > 0:
        res.append(s % base)
        s //= base
    return res[::-1]


class MonoidElem:
    symbols: int
    # mc: MonoidController

    def __init__(self, x: int) -> None:
        self.symbols = x

    def __len__(self):
        l = 0
        x = self.symbols
        while x:
            x //= base
            l += 1
        return l

    def len(self):
        return self.__len__()

    def __getitem__(self, i: int) -> int:
        return decode(self)[i]

    def __repr__(self):
        idxs = decode(self.symbols)
        names = [chr(ord('a') + idx - 1) for idx in idxs]
        return '"' + ''.join(names) + '"'

    def __add__(self, other: MonoidElem):
        if other.is_identity():
            return self
        return MonoidElem(self.symbols * base**len(other) + other.symbols)

    def __eq__(self, other: MonoidElem) -> bool:
        assert isinstance(other, MonoidElem)
        return self.symbols == other.symbols

    def __hash__(self) -> int:
        return hash(str(self.symbols))

    def __lt__(self, o: MonoidElem):
        return self.symbols < o.symbols

    def __gt__(self, o: MonoidElem):
        return self.symbols > o.symbols

    def first(self):
        x = self.symbols
        while x > base:
            x //= base
        return MonoidElem(x)

    def last(self):
        return MonoidElem(self.symbols % base)

    def prefix(self):
        return MonoidElem(self.symbols // base)

    def suffix(self):
        return MonoidElem(
            self.symbols - self.first().symbols * base**(len(self) - 1))

    def to_symbols_seq(self):
        return decode(self)

    @staticmethod
    def from_char(char: int) -> MonoidElem:
        return MonoidElem(encode([char]))

    @staticmethod
    def from_seq(chars: list[int]) -> MonoidElem:
        return MonoidElem(encode(chars))

    @staticmethod
    def identity() -> MonoidElem:
        return MonoidElem(0)

    def is_identity(self):
        return self.symbols == 0

    def letter(self) -> int:
        assert len(self) == 1
        return self.symbols

    # def greedy_value(self) -> Universe:
    #     base_values = [self.mc.generators[i] for i in decode(self.symbols)]
    #     res =

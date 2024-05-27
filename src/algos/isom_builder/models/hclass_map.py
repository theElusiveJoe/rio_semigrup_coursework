from typing import Annotated

from algebra.graph import Hclass, Graph

from algos.control_flow import HclassesMissmatch
from algos.graph_processor.hclasses_searcher import search_Hclasses


def group_hclasses(hclasses: set[Hclass]):
    he, hi, hni = None, dict[int, set[Hclass]](), dict[int, set[Hclass]]()

    for h in hclasses:
        if h.has_e():
            if he is not None:
                raise HclassesMissmatch('too many He')
            else:
                he = h
            continue

        if h.has_idempotent():
            st = hi.get(h.size)
            if st is None:
                st = set()
                hi[h.size] = st
            st.add(h)
            continue

        st = hni.get(h.size)
        if st is None:
            st = set()
            hni[h.size] = st
        st.add(h)

    if he is None:
        raise HclassesMissmatch('didn`t find He')

    return he, hi, hni


class HclassMap:
    _hclasses_map: dict[Hclass, Hclass]

    hi_unmatched: dict[int, Annotated[list[set[Hclass]], 2]]
    hni_unmatched: dict[int, Annotated[list[set[Hclass]], 2]]

    H1: set[Hclass]
    H2: set[Hclass]

    total_num: int

    def __init__(self, initObjects: tuple[Graph, Graph] | None = None) -> None:
        '''
        при создании САМА ставит в соответствие h1_e -> h2_e
        '''
        if initObjects is None:
            return
        G1, G2 = initObjects
        self.H1, self.H2 = set(search_Hclasses(G1)), set(search_Hclasses(G2))

        self.total_num = len(self.H1)

        self._hclasses_map = dict()
        self.hi_unmatched = dict()
        self.hni_unmatched = dict()
        h1e, h1i, h1ni = group_hclasses(self.H1)
        h2e, h2i, h2ni = group_hclasses(self.H2)

        # map He classes
        if h1e.size != h2e.size:
            raise HclassesMissmatch('size of H1e != H2e')
        self._hclasses_map[h1e] = h2e

        if h1i.keys() != h2i.keys():
            raise HclassesMissmatch('sizes of H1i missmatches H2i')
        if h1ni.keys() != h2ni.keys():
            raise HclassesMissmatch('sizes of H1ni missmatches H2ni')

        # set Hclasses as unmapped
        for hsize, s1 in h1i.items():
            s2 = h2i[hsize]
            if len(s1) != len(s2):
                raise HclassesMissmatch(
                    f'neq number of hi-classes of size {hsize}: {len(s1)} vs {len(s2)}')
            self.hi_unmatched[hsize] = [s1, s2]

        for hsize, s1 in h1ni.items():
            s2 = h2ni[hsize]
            if len(s1) != len(s2):
                raise HclassesMissmatch(
                    f'neq number of hni-classes of size {hsize}: {len(s1)} vs {len(s2)}')
            self.hni_unmatched[hsize] = [s1, s2]

    def __str__(self):
        strs = []
        strs.append("HCLASSES_MAP{")
        strs.append("    all_map:")
        for x, y in self._hclasses_map.items():
            strs.append(f'        {x} -> {y}')
        strs.append('}')
        return '\n'.join(strs)

    def assert_current_size(self):
        keys_size = 0
        keys_size += len(self._hclasses_map.keys())
        for v in self.hi_unmatched.values():
            keys_size += len(v[0])
        for v in self.hni_unmatched.values():
            keys_size += len(v[0])
        assert keys_size == self.total_num, f'expected: {self.total_num}, got: {keys_size}'

        values_size = 0
        values_size += len(self._hclasses_map.values())
        for v in self.hi_unmatched.values():
            values_size += len(v[1])
        for v in self.hni_unmatched.values():
            values_size += len(v[1])
        assert values_size == self.total_num

        for size in self.hi_unmatched:
            s1 = set(map(lambda x: x.size, self.hi_unmatched[size][0]))
            s2 = set(map(lambda x: x.size, self.hi_unmatched[size][0]))
            assert (len(s1) == 1 or len(s1) ==
                    0) and s1 == s2, f'hi: size {size}: {s1}, {s2}'

        for size in self.hni_unmatched:
            s1 = set(map(lambda x: x.size, self.hni_unmatched[size][0]))
            s2 = set(map(lambda x: x.size, self.hni_unmatched[size][0]))
            assert len(s1) <= 1 and s1 == s2

    def map_set(self, a: Hclass, b: Hclass):
        remove_here = self.hi_unmatched[a.size] if a.has_idempotent(
        ) else self.hni_unmatched[a.size]
        remove_here[0].remove(a)
        remove_here[1].remove(b)

        self._hclasses_map[a] = b

    def map_get(self, a):
        return self._hclasses_map.get(a)

    def make_copy(self):
        # CMP: можно ли ускорить??
        newMap = HclassMap()
        newMap._hclasses_map = self._hclasses_map.copy()

        newMap.H1, newMap.H2 = self.H1, self.H2
        newMap.hi_unmatched = dict()
        newMap.hni_unmatched = dict()
        for k in self.hi_unmatched.keys():
            newMap.hi_unmatched[k] = [
                self.hi_unmatched[k][0].copy(),
                self.hi_unmatched[k][1].copy()]
        for k in self.hni_unmatched.keys():
            newMap.hni_unmatched[k] = [
                self.hni_unmatched[k][0].copy(),
                self.hni_unmatched[k][1].copy()]

        newMap.total_num = self.total_num
        return newMap

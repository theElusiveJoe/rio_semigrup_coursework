from algebra.universe import Universe
from algebra.monoid import MonoidController
from algebra.graph import Hclass, Graph

from algos.control_flow import HclassesMissmatch


def group_hclasses(hclasses: set[Hclass]):
    he, hi, hni = None, dict[int, set[Hclass]](), dict[int, set[Hclass]]()

    for h in hclasses:
        if h.has_e:
            if he is not None:
                raise HclassesMissmatch('too many He')
            else:
                he = h
            continue

        if h.has_idempotent:
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
        continue

    if he is None:
        raise HclassesMissmatch('didn`t find He')

    return he, hi, hni


class HclassMap:
    hclasses_map: dict[Hclass, Hclass]

    hi_unmatched: dict[int, tuple[set[Hclass], set[Hclass]]]
    hni_unmatched: dict[int, tuple[set[Hclass], set[Hclass]]]

    def __init__(self, initObjects: tuple[set[Hclass], set[Hclass]] | None = None) -> None:
        if initObjects is None:
            return
        h1, h2 = initObjects

        self.hclasses_map = dict()
        h1e, h1i, h1ni = group_hclasses(h1)
        h2e, h2i, h2ni = group_hclasses(h2)

        # map He classes
        if h1e.size != h2e.size:
            raise HclassesMissmatch('size of H1e != H2e')
        self.map_set(h1e, h2e)

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
            self.hi_unmatched[hsize] = (s1, s2)

        for hsize, s1 in h1ni.items():
            s2 = h2ni[hsize]
            if len(s1) != len(s2):
                raise HclassesMissmatch(
                    f'neq number of hni-classes of size {hsize}: {len(s1)} vs {len(s2)}')
            self.hni_unmatched[hsize] = (s1, s2)

    def map_set(self, a: Hclass, b: Hclass):
        # TODO: add check if a or b are already mapped
        self.hclasses_map[a] = b

    def map_get(self, a):
        return self.hclasses_map.get(a)

    def __getitem__(self, key: Hclass):
        return self.hclasses_map[key]

    def make_copy(self):
        newMap = HclassMap()
        newMap.hclasses_map = self.hclasses_map.copy()
        newMap.hi_unmatched = self.hi_unmatched.copy()
        newMap.hni_unmatched = self.hni_unmatched.copy()
        return newMap

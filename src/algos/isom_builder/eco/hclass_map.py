from copy import deepcopy
from typing import Annotated

from algebra.graph import Hclass, Graph

from algos.control_flow import HclassesMissmatch
from algos.graph_processor.hclasses_searcher import search_Hclasses
from algos.isom_builder.shared.algo_config import AlgoConfig
from algos.isom_builder.shared.algo_init_set import AlgoInitSet


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
    images_set: set[Hclass]

    hi_unmatched: dict[int, Annotated[list[set[Hclass]], 2]]
    hni_unmatched: dict[int, Annotated[list[set[Hclass]], 2]]

    H1: set[Hclass]
    H2: set[Hclass]

    config: AlgoConfig

    def __init__(self, init_set: AlgoInitSet | None = None) -> None:
        '''
        при создании САМА ставит в соответствие h1_e -> h2_e
        '''
        if init_set is None:
            return
        self.G1, self.G2 = init_set.G1, init_set.G2
        self.H1, self.H2 = init_set.H1, init_set.H2
        self.config = init_set.config

        self._hclasses_map = dict()
        self.hi_unmatched = dict()
        self.hni_unmatched = dict()
        # CMP: cache_isom_h_images_set
        if self.config.cache_isom_h_images_set:
            self.images_set = set()

        self.prepare()

    def prepare(self):
        h1e, h1i, h1ni = group_hclasses(self.H1)
        h2e, h2i, h2ni = group_hclasses(self.H2)

        # map He classes
        if h1e.size != h2e.size:
            raise HclassesMissmatch('size of H1e != H2e')
        self._hclasses_map[h1e] = h2e
        # CMP: cache_isom_h_images_set
        if self.config.cache_isom_h_images_set:
            self.images_set = set()

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

    def map_set(self, a: Hclass, b: Hclass):
        remove_here = self.hi_unmatched[a.size] if a.has_idempotent(
        ) else self.hni_unmatched[a.size]
        remove_here[0].remove(a)
        remove_here[1].remove(b)
        # CMP: cache_isom_h_images_set
        if self.config.cache_isom_h_images_set:
            self.images_set.add(b)

        self._hclasses_map[a] = b

    def is_image(self, h: Hclass):
        # CMP: cache_isom_h_images_set
        if self.config.cache_isom_h_images_set:
            return h in self.images_set
        return h in self._hclasses_map.values()

    def map_get(self, a):
        return self._hclasses_map.get(a)

    def make_copy(self):
        newMap = HclassMap()

        newMap.H1, newMap.H2 = self.H1, self.H2
        newMap.config = self.config

        newMap._hclasses_map = self._hclasses_map.copy()
        newMap.hi_unmatched = deepcopy(self.hi_unmatched)
        newMap.hni_unmatched = deepcopy(self.hni_unmatched)

        # CMP: cache_isom_h_images_set
        if self.config.cache_isom_h_images_set:
            newMap.images_set = self.images_set

        return newMap

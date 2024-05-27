from algos.isom_builder.models import HclassMap
from algos.isom_builder.models import MonoidMap


class IsomState:
    '''
    это примитивный контейнер, объединяющий граф, моноид контроллер и т.д.
    никакой логики здесь быть не должно!!!
    '''

    f: MonoidMap
    hf: HclassMap

    def make_copy(self):
        newIsomState = IsomState()
        newIsomState.f = self.f.make_copy()
        newIsomState.hf = self.hf.make_copy()
        return newIsomState

    def __str__(self):
        return f'ISOM_STATE:\n{self.f}\n{self.hf}'

    def check_X(self):
        # TODO: remove after debug
        for a, b in self.f.all_map.items():
            assert self.hf.map_get(a.get_hclass()) == b.get_hclass()

        unmatched = set()
        for v in self.hf.hi_unmatched.values():
            unmatched |= v[0]
        for v in self.hf.hni_unmatched.values():
            unmatched |= v[0]

        assert set(self.hf._hclasses_map.keys()
                   ).intersection(unmatched) == set()

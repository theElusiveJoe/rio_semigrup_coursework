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

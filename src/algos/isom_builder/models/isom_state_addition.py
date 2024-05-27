from algebra.graph import Node, Hclass
from . import IsomState


class IsomExtention:
    '''
    эта штука дополняет base_state

    если рассматривать их как одно целое,
    то для этого одного целого должно выполняться ПОЛОЖЕНИЕ Х
    '''
    f: dict[Node, Node]
    hf: dict[Hclass, Hclass]
    base_state: IsomState

    def __init__(self, base_state: IsomState) -> None:
        self.f = dict()
        self.hf = dict()
        self.base_state = base_state

    def _hclasses_are_consistent(
            self, a: Hclass, b: Hclass) -> tuple[bool, bool]:
        '''
        возвращает: (совместимы ли, надо ли добавлять в расшерение base_state)
        '''

        if a.size != b.size:
            return False, False

        a_image = self.base_state.hf.map_get(a)
        # пара (a,b) находится в base_state
        if a_image == b:
            return True, False

        # пара (a, x) находится в base_state
        if a_image != b and a_image is not None:
            return False, False

        # пара (x, b) находится в base_state
        if b in self.base_state.hf._hclasses_map.values():
            return False, False

        # аналогично проверяем для дополнения base_state

        a_image2 = self.hf.get(a)
        # пара (a,b) находится в base_state
        if a_image2 == b:
            return True, False
        if a_image2 != b and a_image2 is not None \
                or b in self.hf.values():
            return False, False

        return True, True

    def _monoid_elems_are_consistent(
            self, a: Node, b: Node) -> tuple[bool, bool]:
        '''
        возвращает: (совместимы ли, надо ли добавлять в расшерение base_state)
        '''

        a_image = self.base_state.f.map_get(a)
        # пара (a,b) находится в base_state
        if a_image == b:
            return True, False

        # пара (a, x) находится в base_state
        # пара (x, b) находится в base_state
        if a_image != b and a_image is not None \
                or b in self.base_state.f.all_map.values():
            return False, False

        # аналогично проверяем для дополнения base_state

        a_image2 = self.f.get(a)
        # пара (a,b) находится в base_state
        if a_image2 == b:
            return True, False
        if a_image2 != b and a_image2 is not None \
                or b in self.f.values():
            return False, False

        return True, True

    def check_and_set_monoid_elems_and_hclasses(
            self, a: Node, b: Node) -> bool:
        a_class, b_class = a.get_hclass(), b.get_hclass()
        # проверяем H-классы на совместимость
        are_consistent_hclasses, should_set = self._hclasses_are_consistent(
            a_class, b_class)
        # если не совместимы, то увы
        if not are_consistent_hclasses:
            return False
        # ставим, если надо
        if should_set:
            assert a_class not in self.hf.keys()
            self.hf[a_class] = b_class

        # если с H-классами все хорошо, то разбираемся с самими элементами
        are_consistent, should_set = self._monoid_elems_are_consistent(a, b)
        if should_set:
            self.f[a] = b
        return are_consistent

    def merge_base_state_and_addition(self) -> IsomState:
        '''
        returns updated copy of base_state
        '''
        newState = self.base_state.make_copy()
        for a, b in self.hf.items():
            newState.hf.map_set(a, b)
            newState.hf.assert_current_size()
        for a, b in self.f.items():
            newState.f.map_set(a, b)
        return newState

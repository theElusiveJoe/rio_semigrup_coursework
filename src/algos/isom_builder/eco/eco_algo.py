from algebra.universe.abstract import Universe

from functools import reduce
from algebra.monoid import MonoidController
from algebra.graph import Graph, Node, Hclass, MultipleType

from algos.graph_builder import military_algo

from algos.control_flow.custom_exceptions import HclassesMissmatch

from algos.isom_builder.shared.algo_config import AlgoConfig
from algos.isom_builder.shared.algo_init_set import AlgoInitSet

from algos.isom_builder.eco.chain import Chain
from algos.isom_builder.eco.chain_winder import ChainWinder
from algos.isom_builder.eco.hclass_map import HclassMap
from algos.isom_builder.eco.isom_state import IsomState
from algos.isom_builder.eco.isom_state_extention import IsomExtention
from algos.isom_builder.eco.monoid_map import MonoidMap
from algos.isom_builder.shared.check import check_isom
from utils.events import spawn_event, Event, event_on_startup


'''
ПОЛОЖЕНИЕ Х
Очень важное общее положение работы алгоритма:
если в state.f стоит a->b
то гарантированно в state.hf стоит H[a] -> H[b]

это очень важно и нужно для всяких consistency чеков

в частности:
    если H[a] -> H[b],
    то не надо для каждого элемента H[a] проверять, что его образ находится в H[b]
'''


'''
Меткой CMP помечаются места, в которых логика работы алгоритма зависит от конфига работы
'''


class IsomBuilderEcoAlgo:
    proto_chains: dict[Node, Chain]
    image_chains: dict[Node, Chain]

    S1: MonoidController
    S2: MonoidController

    G1: Graph
    G2: Graph

    config: AlgoConfig
    init_set: AlgoInitSet

    def __init__(self, init_set: AlgoInitSet):
        self.S1, self.S2, self.G1, self.G2 = init_set.S1, init_set.S2, init_set.G1, init_set.G2
        self.config = init_set.config if init_set.config is not None else AlgoConfig()
        self.init_set = init_set

        self.proto_chains = dict()
        self.image_chains = dict()

    def run(self) -> IsomState | None:
        try:
            start_state = IsomState()

            '''
            e1->e2 в MonoidMap
            и
            h1_e -> h2_e в HclassMap
            ставятся сами
            '''

            start_state.f = MonoidMap(self.init_set)
            start_state.hf = HclassMap(self.init_set)

            return self.guess_elem(start_state)
        except HclassesMissmatch:
            return None

    def get_chain(self, node: Node, from_gs1: bool):
        if from_gs1:
            return self.proto_chains.get(node)
        return self.image_chains.get(node)

    def get_candidate_to_guess(
            self, state: IsomState) -> tuple[Node, Hclass] | None:
        '''
        берем рандомный незаматченный узел из gebeerating_set_1,
        такой, что его hclass уже куда-то матчится

        возвращаем ноду, ее hclass и его образ

        т.е. выбирается x и уже гарантированно H[x] -> H[y] for some y
        '''

        for node in state.f.s1_unmatched_generatos:
            hclass_image = state.hf.map_get(node.get_hclass())
            if hclass_image is None:
                continue
            return (node, hclass_image)

        return None

    def guess_hclass(self, state: IsomState) -> None | IsomState:
        '''
        вызывается только тогда, когда get_candidate_to_guess ничего не выдал
        т.е. для любого узла x из gs1_unmatched_nodes
        H[x] не будет иметь образа
        '''

        a = state.f.s1_unmatched_generatos.pop()
        state.f.s1_unmatched_generatos.add(a)
        a_class = a.get_hclass()

        b_class_image_src = (state.hf.hi_unmatched if a_class.has_idempotent() else state.hf.hni_unmatched)[
            a_class.size][1]

        for b_class in b_class_image_src:

            next_state = state.make_copy()
            '''
            помним ПОЛОЖЕНИЕ Х
            если у H-класса нет образа, то ни у одного его элемента - тоже
            т.е. мы вообще никогда не трогали ни сам класс, ни его элементы
            '''
            next_state.hf.map_set(a_class, b_class)
            if b_class.has_idempotent():
                '''
                ну а какой смысл для двух идемпотентов из 'свеженьких' H-классов
                делать проверку
                проверки у нас цепные, а идемпотенты дают цепь длинны 1
                так что, можно смело ставить
                '''
                # эта строчка нужна, чтобы тайпчекер не ругался
                assert a_class.idempotent is not None and b_class.idempotent is not None
                next_state.f.map_set(a_class.idempotent, b_class.idempotent)

            result_state = self.guess_elem(next_state)
            if result_state is not None:
                return result_state
            continue

        return None

    def check_guess_by_chain(self, state: IsomState,
                             a: Node, b: Node) -> None | IsomState:
        '''
        вызывается, когда хотим проверить, может ли f(a)==b

        если может, то в изоморфизм будут внесены множественные изменения

        a должен быть незаматченным элементом из generating_set_1,
        b должен быть произвольным элементом

        строит цепи a^n и b^n (или берет из кеша)
        '''

        '''
        a приходит из get_candidate_to_guess => точно не заматченный генератор
        проверка b in state.f.all_map.values() проиходит перед вызовом этой функции
        '''

        '''
        и опять же,
        а прилетел из get_candidate_to_guess,
        b взять из guess field
        так что, их H-классы точно совпадают
        '''

        '''
        генерируя цепи, мы можем зайти в новые H-классы
        поэтому нужна функция, проверяющая совместимость двух классов
        этим занимается IsomExtention
        '''

        # CMP: cache_proto_chains
        match self.config.cache_proto_chains:
            case True:
                a_chain = self.get_chain(a, True)
                if a_chain is None:
                    a_chain = Chain(a, MultipleType.generator, self.G1)
                    self.proto_chains[a] = a_chain
            case False:
                a_chain = Chain(a, MultipleType.generator, self.G1)

        # CMP: cache_image_chains
        match self.config.cache_image_chains:
            case True:
                b_chain = self.get_chain(b, False)
                if b_chain is None:
                    # CMP: second_chain_mult_type
                    b_chain = Chain(
                        b, self.config.second_chain_mult_type, self.G2)
                    self.image_chains[b] = b_chain
            case False:
                # CMP: second_chain_mult_type
                b_chain = Chain(b, self.config.second_chain_mult_type, self.G2)

        # если обе цепи уже построены, то для их совместности необходимо
        # равенство их длинн
        if a_chain.is_completed and b_chain.is_completed:
            if a_chain.len() != b_chain.len():
                return None

        state_extention = IsomExtention(state)
        a_winder, b_winder = ChainWinder(a_chain), ChainWinder(b_chain)

        res = None
        n = 0
        while True:
            n += 1

            an, bn = a_winder.next(), b_winder.next()

            are_consistent = state_extention.check_and_set_monoid_elems_and_hclasses(
                an, bn)

            # цепи не своместны в state+state_extention
            if are_consistent == False:
                res = None
                break

            # одна цепь зациклилась, а другая - нет
            if a_winder.at_the_end() != b_winder.at_the_end():
                res = None
                break

            # обе цепи завершились одновременно, причем все их элементы
            # совпадали
            if a_winder.at_the_end() == b_winder.at_the_end() == True:
                res = state_extention.merge_base_state_and_extention()
                break

        return res

    def guess_elem(self, state: IsomState) -> None | IsomState:
        if state.f.is_gen_set_done():
            ok = self.check(state)
            if ok:
                return state
            return None

        guess_field = self.get_candidate_to_guess(state)
        if guess_field is None:
            return self.guess_hclass(state)

        a, hb = guess_field
        for b in hb.elems:
            if state.f.is_image(b):
                continue

            next_state = self.check_guess_by_chain(state, a, b)

            if next_state is not None:
                final_state = self.guess_elem(next_state)
                if final_state is not None:
                    return final_state

        return None

    def check(self, state: IsomState) -> IsomState | None:
        if check_isom(self.init_set, state):
            return state
        return None
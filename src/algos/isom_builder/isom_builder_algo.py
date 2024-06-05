from algebra.universe.abstract import Universe

from functools import reduce
from algebra.monoid import MonoidController
from algebra.graph import Graph, Node, Hclass, MultipleType

from algos.graph_builder import military_algo

from algos.control_flow.custom_exceptions import HclassesMissmatch
from algos.isom_builder.models import IsomState, IsomExtention
from algos.isom_builder.models import MonoidMap, HclassMap
from algos.isom_builder.models import Chain, ChainWinder
from algos.isom_builder.models import AlgoConfig, AlgoInitSet

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


class IsomBuilderAlgo:
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
        match self.config.cache_proto_chains:
            case True:
                b_chain = self.get_chain(b, False)
                if b_chain is None:
                    # CMP: second_chain_mult_type
                    b_chain = Chain(
                        b, self.config.second_chain_mult_type, self.G2)
                    self.proto_chains[b] = b_chain
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

            # CMP: chain_max_len
            if n > self.config.chain_max_len:
                res = state_extention.merge_base_state_and_addition()
                break

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
                res = state_extention.merge_base_state_and_addition()
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

    def check(self, state: IsomState) -> bool:
        total_map: dict[Universe, Universe] = dict()

        '''
        строим моноид из образов generating_set_1
        проверяем, что рамеры графов совпадают
        '''
        gs2 = list(map(lambda x: x.val, state.f.gen_set_map.values()))
        image_mc = MonoidController(gs2)
        image_graph = military_algo(image_mc)
        if len(self.G1.nodes) != len(image_graph.nodes):
            return False

        for a in self.G1.nodes:
            for b in self.G1.nodes:
                ab_val = a.val * b.val
                # найдем разложение a на элементы generating_set_1
                a_decomp = [self.G1.val2node[x]
                            for x in self.S1.symbols_to_values(a.str.to_symbols_seq())]
                # найдем разложение b на элементы generating_set_1
                b_decomp = [self.G1.val2node[x]
                            for x in self.S1.symbols_to_values(b.str.to_symbols_seq())]
                # разложение ab
                ab_decomp = a_decomp + b_decomp

                if ab_decomp == [] and ab_val.is_identity():
                    continue

                # список образов разложения ab
                ab_decomp_image = [state.f.all_map[x] for x in ab_decomp]
                # перемножим
                ab_val_image = reduce(
                    lambda x, y: x * y.val, ab_decomp_image[1:], ab_decomp_image[0].val)

                ab_val_exists_image = total_map.get(ab_val)
                if ab_val_exists_image is None:
                    total_map[ab_val] = ab_val_image
                else:
                    if ab_val_exists_image != ab_val_image:
                        return False

        return True

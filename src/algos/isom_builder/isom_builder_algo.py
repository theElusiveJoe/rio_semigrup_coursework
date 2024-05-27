from pprint import pformat
import re
import stat

from numpy import imag
from algebra.universe.abstract import Universe
from utils.printer import myprint
from functools import reduce

from algebra.monoid import MonoidController
from algebra.graph import Graph, Node, Hclass
from algos.graph_builder import military_algo
from algos.graph_processor import search_Hclasses, markup_idempotents, search_generating_nodes

from algos.isom_builder.models import IsomState, IsomExtention
from algos.isom_builder.models import MonoidMap, HclassMap
from algos.isom_builder.models import Chain, ChainWinder, ChainMultipleType


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
Меткой CMP помечаются места, которые можно сделать по-другому,
что может пригодиться на стадии тестирования
'''


class IsomBuilderAlgo:
    chains: dict[Node, Chain]
    gs1_chains: dict[Node, Chain]

    S1: MonoidController
    S2: MonoidController

    G1: Graph
    G2: Graph

    # H1: set[Hclass]
    # H2: set[Hclass]

    def __init__(self, S1: MonoidController, S2: MonoidController, G1: Graph, G2: Graph):
        if len(S1) > len(S2):
            self.S1, self.S2, self.G1, self.G2 = S2, S1, G2, G1
        else:
            self.S1, self.S2, self.G1, self.G2 = S1, S2, G1, G2

        self.chains = dict()
        self.gs1_chains = dict()

    def run(self) -> IsomState | None:
        start_state = IsomState()

        '''
        необходимо явно ставить e1->e2 в MonoidMap
        это связано с тем, что IsomState не хранит ссылки на граф и моноид

        в HclassMap ставить h1_e -> h2_e не надо
        при инициализации она проводит сортировку H-классов, и сама находит h1_e и H2_e
        '''

        start_state.f = MonoidMap((self.S1, self.G1))
        start_state.f.map_set(
            self.G1.val2node[self.S1.identity()], self.G2.val2node[self.S2.identity()])

        markup_idempotents(self.G1)
        markup_idempotents(self.G2)
        start_state.hf = HclassMap((self.G1, self.G2))

        return self.guess_elem(start_state)

    def get_chain(self, node: Node, from_gs1: bool):
        if from_gs1:
            return self.gs1_chains.get(node)
        return self.chains.get(node)

    def get_candidate_to_guess(self, state: IsomState) -> tuple[Node, Hclass] | None:
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

    def check_guess_by_chain(self, state: IsomState, a: Node, b: Node) -> None | IsomState:
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

        a_chain, b_chain = self.get_chain(a, True), self.get_chain(b, False)
        if a_chain is None:
            a_chain = Chain(a, ChainMultipleType.generator, self.G1)
            # добавляем цепь в кэш
            self.gs1_chains[a] = a_chain
        if b_chain is None:
            # CMP: try with ChainMultipleType.monoid_multiply
            b_chain = Chain(b, ChainMultipleType.graph_traverse, self.G2)
            self.chains[b] = b_chain

        # если обе цепи уже построены, то для их совместности необходимо равенство их длинн
        if a_chain.is_completed and b_chain.is_completed:
            if a_chain.len() != b_chain.len():
                return None

        state_extention = IsomExtention(state)
        a_winder, b_winder = ChainWinder(a_chain), ChainWinder(b_chain)

        res = None
        while True:
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

            # обе цепи завершились одновременно, причем все их элементы совпадали
            if a_winder.at_the_end() == b_winder.at_the_end() == True:
                res = state_extention.merge_base_state_and_addition()
                break

        return res

    def guess_elem(self, state: IsomState) -> None | IsomState:
        state.hf.assert_current_size()

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
            # CMP: try to make it faster!!!
            if b in state.f.all_map.values():
                continue

            next_state = self.check_guess_by_chain(state, a, b)

            if next_state is not None:
                final_state = self.guess_elem(next_state)
                if final_state is not None:
                    return final_state

        return None

    # def check(self, state: IsomState) -> bool:
    #     '''
    #     способ1 -- работает для автоморфизмов
    #     строим моноид из образов generating_set_1
    #     проверяем, что рамеры графов совпадают
    #     '''
    #     # print('check')
    #     # print(state.f)

    #     gs2 = list(map(lambda x: x.val, state.f.gen_set_map.values()))
    #     image_mc = MonoidController(gs2)
    #     image_graph = military_algo(image_mc)
    #     if len(self.G1.nodes) != len(image_graph.nodes):
    #         # print(self.G1.nodes)
    #         # print(image_graph.nodes)
    #         # print('not a gen set')
    #         return False

    #     '''
    #     gs1 - generating_set_1
    #     gs2 - generating_set_2
    #     gs1_images - f(gs1)

    #     разложим gs1_images по gs2
    #     \forall a,b \in gs1 проверимx, что:
    #         f(a)*f(b) = 
    #     '''

    #     print(state.f)
    #     for a, a_img in state.f.gen_set_map.items():
    #         for b, b_img in state.f.gen_set_map.items():
    #             # print(f'try {a}*{b}')

    #             var1 = a_img.val * b_img.val
    #             # print(f'f({a})*f({b}) = {var1} = {self.G2.val2node[var1]}')

    #             ab_decomp_values = self.S1.symbols_to_values(
    #                 self.G1.val2node[a.val * b.val].str.to_symbols_seq()
    #             )
    #             # скорее всего, получим те же [a, b], но не всегда и это важно
    #             ab_decomp_nodes = list(self.G1.val2node[x] for x in ab_decomp_values)
    #             if ab_decomp_nodes == [a,b]:
    #                 continue

    #             if ab_decomp_nodes == [] and var1.is_identity():
    #                 return True
                
    #             # print(a,b)
    #             # print(f'{a}*{b} = {self.G1.val2node[a.val * b.val]} = {self.G1.val2node[a.val * b.val].str.to_symbols_seq()} = {ab_decomp_nodes}')
    #             ab_decomp_nodes_images = list(state.f.all_map[x] for x in ab_decomp_nodes)
    #             var2 = reduce(lambda x,y: x*y.val, ab_decomp_nodes_images[1:], ab_decomp_nodes_images[0].val)
    #             # print(f'f({a}*{b}) = f({ab_decomp_nodes}) = f.{ab_decomp_nodes_images} = {self.G2.val2node[var2]}')
    #             # assert False
    #             if var1 != var2:
    #                 return False
        
    #     print('ok!!')
    #     return True


    def check(self, state: IsomState) -> bool:
        total_map: dict[Universe, Universe] = dict()
        # print('GO SHALLOW CHECK IN ALGO')

        gs2 = list(map(lambda x: x.val, state.f.gen_set_map.values()))
        image_mc = MonoidController(gs2)
        image_graph = military_algo(image_mc)
        if len(self.G1.nodes) != len(image_graph.nodes):
            # print(self.G1.nodes)
            # print(image_graph.nodes)
            # print('not a gen set')
            # print('    SHALLOW CHECK FAILED')
            return False

        # print('GO DEEP CHECK IN ALGO')
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
                ab_val_image = reduce(lambda x,y: x * y.val, ab_decomp_image[1:], ab_decomp_image[0].val)

                ab_val_exists_image = total_map.get(ab_val)
                if ab_val_exists_image is None:
                    total_map[ab_val] = ab_val_image
                else:
                    if ab_val_exists_image != ab_val_image: 
                        # print('    DEEP CHECK FAILED')
                        return False
        
        print('ALGO CHECK PASSED')
        return True

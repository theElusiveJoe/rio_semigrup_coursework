from functools import reduce
from itertools import chain
from xml.etree.ElementTree import QName

from graphviz import Graph

from algebra.graph.graph import MultipleType
from algebra.monoid.controller import MonoidController
from algebra.universe.abstract import Universe
from algos.graph_builder import military_algo
from algebra.graph.node import Node
from algos.isom_builder.eco.isom_state import IsomState
from algos.isom_builder.naive.simple_isom import SimpleIsom
from utils.events.event import Event
from utils.events.eventsHandler import event_on_startup
from .algo_init_set import AlgoInitSet


def ch_monoid_mult(init_set: AlgoInitSet, isom: IsomState | SimpleIsom) -> bool:
    total_map: dict[Universe, Universe] = dict()

    for a in init_set.G1.nodes:
        a_decomp = [init_set.G1.val2node[x]
                    for x in init_set.S1.symbols_to_values(a.str.to_symbols_seq())]

        if type(isom) == IsomState:
            a_decomp_image = [isom.f.gen_set_map[x] for x in a_decomp]
        elif type(isom) == dict:
            a_decomp_image = [isom[x] for x in a_decomp]
        else:
            raise RuntimeError(f'unknown isom type: {isom}:{type(isom)}')

        total_map[a.val] = reduce(lambda x, y: x * y.val,
                                  a_decomp_image, init_set.S2.identity())

    for a, a_img in total_map.items():
        for b, b_img in total_map.items():
            if a_img * b_img != total_map[a*b]:
                return False
    return True


def ch_graph_traverse(init_set: AlgoInitSet, isom: IsomState | SimpleIsom) -> bool:
    total_map: dict[Node, Node] = dict()

    for a in init_set.G1.nodes:
        a_decomp = [init_set.G1.val2node[x]
                    for x in init_set.S1.symbols_to_values(a.str.to_symbols_seq())]

        if type(isom) == IsomState:
            a_decomp_image = [isom.f.gen_set_map[x] for x in a_decomp]
        elif type(isom) == dict:
            a_decomp_image = [isom[x] for x in a_decomp]
        else:
            raise RuntimeError(f'unknown isom type: {isom}:{type(isom)}')

        if a_decomp_image == []:
            a_img = init_set.G2.val2node[init_set.S2.identity()]
        else:
            traverse_path = init_set.S2.symbols_to_values(
                list(chain(*map(
                    lambda x: x.str.to_symbols_seq(),
                    a_decomp_image[1:]
                )))
            )
            a_img = reduce(
                lambda x, y: x.cay_r[y], traverse_path, a_decomp_image[0])

        total_map[a] = a_img

    for a, a_img in total_map.items():
        for b, b_img in total_map.items():

            mult_of_images = reduce(
                lambda x, y: x.cay_r[y],
                init_set.S2.symbols_to_values(b_img.str.to_symbols_seq()),
                a_img
            )

            image_of_mult = total_map[
                reduce(
                    lambda x, y: x.cay_r[y],
                    init_set.S1.symbols_to_values(b.str.to_symbols_seq()),
                    a
                )
            ]

            if mult_of_images != image_of_mult:
                return False

    return True


def ch3(init_set: AlgoInitSet, isom: IsomState | SimpleIsom) -> bool:
    # CMP: second_chain_mult_type
    if init_set.config.second_chain_mult_type == MultipleType.monoid_multiply:
        return ch_monoid_mult(init_set, isom)
    else:
        return ch_graph_traverse(init_set, isom)


@event_on_startup(Event.check_call)
def check_isom(init_set: AlgoInitSet, isom: IsomState | SimpleIsom) -> bool:
    '''
    строим моноид из образов generating_set_1
    проверяем, что рамеры графов совпадают
    '''
    # if type(isom) == IsomState:
    #     gs2 = list(map(lambda x: x.val, isom.f.gen_set_map.values()))
    # elif type(isom) == dict:
    #     gs2 = list(map(lambda x: x.val, isom.values()))
    # else:
    #     raise RuntimeError(f'unknown isom type:{type(isom)}')

    # image_mc = MonoidController(gs2)
    # image_graph = military_algo(image_mc)
    # if len(init_set.G1.nodes) != len(image_graph.nodes):
    #     return False
    return ch3(init_set, isom)

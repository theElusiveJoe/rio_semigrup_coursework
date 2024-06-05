from algebra.monoid import MonoidController
from algebra.graph import Node, Graph
from algos.isom_builder.models.algo_config import AlgoConfig
from algos.isom_builder.models.algo_init_set import AlgoInitSet


class MonoidMap:
    S1: MonoidController
    G1: Graph

    all_map: dict[Node, Node]
    gen_set_map: dict[Node, Node]

    s1_unmatched_generatos: set[Node]
    images_set: set[Node]

    config: AlgoConfig

    def __init__(
            self, init_set: AlgoInitSet | None = None) -> None:
        if init_set is None:
            return

        self.S1, self.G1 = init_set.S1, init_set.G1
        self.all_map = dict()
        self.gen_set_map = dict()
        self.s1_unmatched_generatos = set(
            [self.G1.val2node[val] for val in self.S1.generators])

        self.config = init_set.config

        # CMP: cache_isom_images_set
        if self.config.cache_isom_images_set:
            self.images_set = set()

        self.map_set(
            self.G1.val2node[self.S1.identity()], init_set.G2.val2node[init_set.S2.identity()])

    def __str__(self):
        strs = []
        strs.append("MONOID_MAP{")
        strs.append("    gen_set_map:")
        for x, y in self.gen_set_map.items():
            strs.append(f'        {x} -> {y}')
        strs.append('}')
        return '\n'.join(strs)

    def is_gen_set_done(self):
        return len(self.s1_unmatched_generatos) == 0

    def map_set(self, a: Node, b: Node):
        # remove from unmatched generator, if there
        is_generator = True
        try:
            self.s1_unmatched_generatos.remove(a)
        except KeyError:
            is_generator = False

        self.all_map[a] = b
        if is_generator:
            self.gen_set_map[a] = b

        # CMP: cache_isom_images_set
        if self.config.cache_isom_images_set:
            self.images_set.add(b)

    def map_get(self, a: Node):
        return self.all_map.get(a)

    def is_image(self, x: Node) -> bool:
        # CMP: cache_isom_images_set
        if self.config.cache_isom_images_set:
            return x in self.images_set
        else:
            return x in self.all_map.values()

    def make_copy(self):
        newMap = MonoidMap()

        newMap.S1 = self.S1
        newMap.config = self.config

        newMap.all_map = self.all_map.copy()
        newMap.s1_unmatched_generatos = self.s1_unmatched_generatos.copy()
        newMap.gen_set_map = self.gen_set_map.copy()

        # CMP: cache_isom_images_set
        if self.config.cache_isom_images_set:
            newMap.images_set = self.images_set.copy()

        return newMap
